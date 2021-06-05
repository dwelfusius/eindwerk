import requests
import json
from environment import int_report as env
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta as delta
from pandas import pandas as pd, to_datetime as todate
from urllib.parse import urlencode
import time as tm
from collections import Counter

fail_req = []


def get_mailaddress(pages):
    """get_mailaddress Iterates over webex people api responses 

    :param pages: http response pages
    :type pages: dict
    :return: a list of unique emailadresses
    :rtype: list
    """

    list_mails = []
    for page in pages:
        for p in page["items"]:
            list_mails.append(p["emails"][0])
    return list_mails


def pages_list(url):
    """pages_list Performs a GET against the passed url and potential 
    next pages. Returns the response text in json if available, logs
    error code on fail

    :param url: url with parameters encoded via urllib
    :type url: str
    :yield: response text from request
    :rtype: json
    """
    f_page = requests.get(url, headers=env['headers'])
    if f_page.status_code == 200:
        yield f_page.json()
        if 'next' in f_page.links:
            page = f_page.links['next']['url']
            while page:
                n_page = requests.get(page, headers=env['headers'])
                if n_page.status_code == 200:
                    yield n_page.json()
                    if 'next' in n_page.links:
                        page = n_page.links['next']['url']
                    else:
                        page = False
    else:
        fail_req.append(f_page.status_code)


def part_list(meetingId):
    """part_list Performs a GET to retrieve participants of the 
    passed meeting. Returns them as a list if available, 
    logs error code on fail

    :param meetingId: a webex meeting ID
    :type meetingId: str
    :return: the items key value from the get request
    :rtype: list
    """
    url = "https://webexapis.com/v1/meetingParticipants"
    uri = f"{url}?meetingId={meetingId}"
    participants = requests.get(uri, headers=env['headers'])
    if participants.status_code == 200:
        part_dict = json.loads(participants.text)
        return(part_dict["items"])
    else:
        fail_req.append(participants.status_code)
        return None


def get_part_stats(m):
    """get_part_stats Calculate amount of participants and minutes in 
    meeting info of passed meeting.

    :param m: a list of dictionaries with meeting details
    :type m: list
    :return: calculated participant count and attendance per meeting
    :rtype: dict
    """
    parts = (part_list(m.id))
    if parts:
        parts_df = pd.DataFrame()
        for part in parts:
            parts_df = parts_df.append(
                part['devices'][0],
                ignore_index=True
            )
        parts_df['joinedTime'] = todate(parts_df['joinedTime'])
        parts_df['leftTime'] = todate(parts_df['leftTime'])
        parts_df['delta'] = parts_df.apply(
            lambda r: pd.Timedelta
            (r.leftTime - r.joinedTime).seconds
            / 60.0, axis=1
        )
        part_stats_dict = {
            'Participant_Min': parts_df['delta'].sum(),
            'Participants': len(parts_df)
        }
        return part_stats_dict
    else:
        return {}


def get_param(time_unit='days', age=int(14)):
    """get_param morph the needed parameter values in into a dict object
    to use in the api request

    :param time_unit: time measurement to use, defaults to 'days'
                    hours,days,weeks,months (plural!) are all valid
    :type time_unit: str, optional
    :param age: to substract in time unit from today, defaults to int(14)
    :type age: int, optional
    :return: dictionary with parameter values
    :rtype: dict
    """
    date_d = delta(**{time_unit: age.__neg__()})
    date = dt.today() + delta(days=+1)
    param_dict = {
        'to': date.strftime(format='%Y-%m-%d'),
        'from': (date + date_d).strftime(format='%Y-%m-%d'),
        'siteUrl': env['siteUrl'],
        'max': 100
    }
    return param_dict


def get_meeting(m):
    """get_meeting Create a dictionary from passed meeting

    :param m: a list of dictionaries with meeting details
    :type m: list
    :return: dictionary with meeting information
    :rtype: dict
    """
    mt_dict = {
        'id': m.id,
        'day': dt.strftime(m.start, format='%d/%m/%Y'),
        'start': m.start,
        'end': m.end,
        'meetingType': 'meeting'
    }
    return mt_dict


def get_stats_df(meetings_df):
    """get_stats_df Copy passed DataFrame,use it to calculate totals
    and averages per day/meeting/participants, sort, adds a total rows
    and export as DF

    :param meetings_df: DataFrame with all meetings and participant totals
    :type df: DataFrame
    :return: calculated and sorted meeting statistics
    :rtype: DataFrame
    """
    if not meetings_df.empty:
        cp_df = meetings_df.copy(deep=True)
        cp_df.fillna(0, inplace=True, downcast='infer')
        df_dict = {}

        for day in cp_df['day'].unique():
            c_df = cp_df[cp_df['day'] == day].reset_index()
            c_df['delta'] = c_df.apply(
                lambda r: pd.Timedelta
                (r.end - r.start).seconds
                / 60.0, axis=1
            )
            tot_part_min = c_df.sum().Participant_Min
            tot_part = c_df.sum().Participants
            tot_part_val = tot_part if tot_part > 0 else 1
            tot_meet = c_df.count().id
            df_dict[day] = {
                'Day': todate(day).day_name(),
                'Date': todate(day, format='%d/%m/%Y'),
                'Total_Meetings': c_df.count().day,
                'Total_Meeting_Min': int(c_df['delta'].sum()),
                'Avg_Meeting_Min': int(c_df['delta'].sum()/tot_meet),
                'Total_Participants': c_df.sum().Participants,
                'Total_Participant_Min': int(tot_part_min),
                'Avg_Participants_Min': int(tot_part_min/tot_part_val),
                'Avg_Part_Min_Meeting': int(
                    (tot_part_min/tot_part_val)/tot_meet)
            }
        stat_df = pd.DataFrame(df_dict.values()).sort_values('Date')
        stat_df['Date'] = stat_df['Date'].apply(
            lambda x: dt.strftime(x, format='%d/%m/%Y'))

        totals_dict = {
            'Day': 'Total',
            'Date': str(stat_df.Date.count())+' days',
            'Total_Meetings': stat_df.Total_Meetings.sum(),
            'Total_Meeting_Min': stat_df.Total_Meeting_Min.sum(),
            'Avg_Meeting_Min': int(
                stat_df.Avg_Meeting_Min.sum()/stat_df.Date.count()),
            'Total_Participants': stat_df.Total_Participants.sum(),
            'Total_Participant_Min': int(
                stat_df.Total_Participant_Min.sum()),
            'Avg_Participants_Min': int(
                stat_df.Total_Participant_Min.sum()
                /stat_df.Total_Participants.sum()),
            'Avg_Part_Min_Meeting': int(
                (stat_df.Total_Participant_Min.sum()
                /stat_df.Total_Participants.sum())
                /stat_df.Total_Meetings.count())
        }
        stat_df = stat_df.append(totals_dict,ignore_index=True)
        return stat_df
    else:
        return meetings_df


def main():
    begin_time = dt.now()
    print(dt.now())
    url = "https://webexapis.com/v1/"
    print('---Retrieve list of people---')
    people_list = get_mailaddress(pages_list(f'{url}people'))
    param_dict = get_param(time_unit='months', age=1)
    mt_df = pd.DataFrame()
    print(dt.now() - begin_time)
    print('---Retrieve meetings per person---')
    for person in people_list:
        param_dict['hostEmail'] = person
        uri = f"{url}meetings?{urlencode(param_dict)}"
        pages = pages_list(uri)
        for page in pages:
            p_df = pd.DataFrame(page["items"])
            if not p_df.empty:
                p_df['start'] = todate(p_df['start'])
                p_df['end'] = todate(p_df['end'])
                for mt in p_df.iterrows():
                    tm.sleep(2)
                    mt_row = mt[1]
                    mt_dict = get_meeting(mt_row)
                    part_dict = get_part_stats(mt_row)
                    dict = {**part_dict, **mt_dict}
                    mt_df = mt_df.append(dict, ignore_index=True)
    print(dt.now() - begin_time)
    print('---Calculate statistics---')
    mts_df = get_stats_df(mt_df)
    print(dt.now() - begin_time)
    mts_df.to_excel(
        f'meeting_stats_{param_dict["from"]}-{param_dict["to"]}.xlsx',
        sheet_name='meetings', index=False
    )
    if not len(fail_req) == 0:
        print(Counter(fail_req))


# execute main when called directly
if __name__ == '__main__':
    main()
