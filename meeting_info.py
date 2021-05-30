import requests
import json
from environment import biasc as env
#from environment import int_report as env
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta as delta
from pandas import pandas as pd,to_datetime as todate
from urllib.parse import urlencode
import time as tm

def get_emails(pages):
    list_mails = []
    for page in pages:
        for p in page["items"]:
            list_mails.append(p["emails"][0])
    return list_mails

def pages_list(url):
    f_page = requests.get(url,headers=env['headers'])
    if f_page.status_code==200:
        yield f_page.json()
        if 'next' in f_page.links:
            page = f_page.links['next']['url']
            while page:
                n_page = requests.get(page,headers=env['headers'])
                if n_page.status_code==200:
                    yield n_page.json()
                    if 'next' in n_page.links:
                        page = n_page.links['next']['url']
                    else:
                        page = False
    else:
        print(f_page.status_code, 'Meeting', f_page.reason)


def part_list(meetingId):
    url = f"https://webexapis.com/v1/meetingParticipants?meetingId={meetingId}"
    response = requests.get(url, headers=env['headers'])
    if response.status_code==200:
        dict = json.loads(response.text)
        return(dict["items"])
    else:
        print(response.status_code, f'- Meeting Participants {meetingId}', response.reason)
        return None

def get_part_stats(m):
    part = (part_list(m.id))
    if part:
        part_df = pd.DataFrame()
        for p in part:
            part_df = part_df.append(p['devices'][0], ignore_index=True)
        part_df['joinedTime'] = todate(part_df['joinedTime'])
        part_df['leftTime'] = todate(part_df['leftTime'])
        part_df['delta']= part_df.apply(lambda r: pd.Timedelta(r.leftTime - r.joinedTime).seconds / 60.0, axis=1)
        part_dict = {
        'Participant_Min': part_df['delta'].sum(),
        'Participants': len(part_df)
        }
        return part_dict
    else:
        return {}


def get_param(t_unit='days',age=14):
    date_d = delta(**{t_unit: age.__neg__() }) 
    date   = dt.today() + delta(days=+1)
    param_dict = {
        'to': date.strftime(format='%Y-%m-%d'),
        'from': (date + date_d).strftime(format='%Y-%m-%d'),
        'siteUrl': env['siteUrl'],
        'max': 100
    }
    return param_dict

def get_meeting(m):
    mt_dict = {
        'id': m.id,
        'day' : dt.strftime(m.start, format='%d/%m/%Y'),
        'start': m.start,
        'end': m.end,
        'meetingType': 'meeting'
    }
    return mt_dict

def get_stats_df(df):
    if not df.empty:
        cp_df = df.copy(deep=True)
        cp_df.fillna(0, inplace=True, downcast='infer')
        df_dict = {}
        for day in cp_df['day'].unique():
            subset = cp_df[cp_df['day']==day].reset_index()
            subset['delta'] = subset.apply(lambda r: pd.Timedelta(r.end - r.start).seconds / 60.0, axis=1)
            tot_part_min = subset.sum().Participant_Min
            tot_part_calc = subset.sum().Participants if subset.sum().Participants>0 else 1
            df_dict[day] = {
            'Day': todate(day).day_name(),
            'Date': todate(day, format='%d/%m/%Y'),
            'Total_Meetings': subset.count().day,
            'Total_Meeting_Min': int(subset['delta'].sum()),
            'Avg_Meeting_Min': int(subset['delta'].sum()/subset.count().id),
            'Total_Participants': subset.sum().Participants,
            'Total_Participant_Min': int(tot_part_min),
            'Avg_Participants_Min': int(tot_part_min/tot_part_calc),
            'Avg_Part_Min_Meeting': int((tot_part_min/tot_part_calc)/subset.count().id)
            }
        stat_df = pd.DataFrame(df_dict.values()).sort_values('Date')
        stat_df['Date'] = stat_df['Date'].apply(lambda x: dt.strftime(x,format='%d/%m/%Y'))
        
        return stat_df
    else:
        return df


def main():
    begin_time = dt.now()
    print(dt.now())
    url = "https://webexapis.com/v1/"
    print('---Retrieve list of people---')
    people_list  = get_emails(pages_list(f'{url}people'))
    param_dict = get_param(t_unit='months',age=1)
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
                    dict = {**part_dict,**mt_dict}
                    mt_df = mt_df.append(dict, ignore_index=True)
    print(dt.now() - begin_time)
    print('---Calculate statistics---')
    mts_df = get_stats_df(mt_df)
    print(dt.now() - begin_time)
    mts_df.to_excel(f'meeting_stats_{param_dict["from"]}-{param_dict["to"]}.xlsx',sheet_name='meetings',index=False)
    
# execute main when called directly
if __name__ == '__main__':
    main()
