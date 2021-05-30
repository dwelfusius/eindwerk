import requests
import json
from environment import biasc as env
#from environment import int_report as env
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta as delta
from pandas import pandas as pd,to_datetime as pan_dt
from urllib.parse import urlencode
import time as tm
from timeit import Timer



def parse_time(cols, df):
    col_list = []
    for c in cols:
        col_list.append(pan_dt(df[c]))
    return col_list


def get_emails_excel(emails):
    df = pd.DataFrame()
    df['people'].append(emails)
    df.to_excel(f'people.xlsx',sheet_name='people',index=False)

def get_emails(pages):
    list_mails = []
    for page in pages:
        for p in page["items"]:
            list_mails.append(p["emails"][0])
    print('---3-- ok')
    return list_mails

def pages_list(url):
    f_page = requests.get(url,headers=env['headers'])
    if f_page.status_code==200:
        #print('---1-- ok')
        yield f_page.json()
        if 'next' in f_page.links:
            page = f_page.links['next']['url']
            while page:
                n_page = requests.get(page,headers=env['headers'])
                if n_page.status_code==200:
                    #print('---2-- ok')
                    yield n_page.json()
                    if 'next' in n_page.links:
                        page = n_page.links['next']['url']
                    else:
                        page = False
    else:
        print('---1-- NoK')
        print(f_page.status_code,f_page.url, f_page.reason)


def part_list(meetingId):
    url = f"https://webexapis.com/v1/meetingParticipants?meetingId={meetingId}"
    response = requests.get(url, headers=env['headers'])
    if response.status_code==200:
        dict = json.loads(response.text)
        #print('ok')
        return(dict["items"].__iter__())
    else:
        print(response.status_code,response.url, response.reason)
        return None

def get_part_stats(m):
    part = (part_list(m.id))
    if part:
        part_df = pd.DataFrame()
        trigger = True
        while trigger:
            try:
                dict = next(part)
                part_df = part_df.append((dict['devices'][0]), ignore_index=True)
            except:
                trigger=False             
        #part_df['joinedTime'],part_df['leftTime'] = parse_time(['joinedTime','leftTime'],part_df)
        pan_dt(part_df['joinedTime'], inplace=True)
        pan_dt(part_df['leftTime'], inplace=True)
        mins = 0
        for i in part_df.itertuples():
            mins += pd.Timedelta(i.leftTime - i.joinedTime).seconds / 60.0
        part_dict = {
        'Participant_Min': int(mins),
        'Participants': len(part_df)
            }
        return part_dict
    else:
        print('Nok part')
        return {}


def get_param(age_month):
    date_d = delta(days=-4)    
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
        'end': m.end
    }
    return mt_dict

def get_stats_df(df):
    cp_df = df.copy(deep=True)
    cp_df.fillna(0, inplace=True, downcast='infer')
    df_dict = {}
    for day in cp_df['day'].unique():
        subset = cp_df[cp_df['day']==day].reset_index()
        mins = 0
        df_dict[day] = {
        'Day': day,
        'Total_Meetings': subset.count().day,
        'Total_Meeting_Min': mins + pd.Timedelta(subset.end[0] - subset.start[0]).seconds / 60, 
        'Total_Participants': subset.sum().Total_Participants,
        'Total_Participant_Min': subset.sum().Total_Participant_Min,
        'Total_Participants': subset.sum().Total_Participants}
    stat_df = pd.DataFrame(df_dict.values(), ignore_index=True)
    return stat_df


def main():
    t = Timer()
    #people_list = pd.read_excel('people.xlsx')['people'].tolist()
    url = "https://webexapis.com/v1/"
    people_list  = get_emails(pages_list(f'{url}people'))
    param_dict = get_param(age_month=3)
    mt_df = pd.DataFrame()
    for person in people_list:
        param_dict['hostEmail'] = person
        uri = f"{url}meetings?{urlencode(param_dict)}"
        pages = pages_list(uri)
        for page in pages:
            p_df = pd.DataFrame(page["items"])
            if not p_df.empty:
                p_df['start'],p_df['end'] = parse_time(['start','end'],p_df)
                for mt in p_df.iterrows():
                    tm.sleep(2)
                    mt_row = mt[1]
                    mt_dict = get_meeting(mt_row)
                    part_dict = get_part_stats(mt_row)
                    dict = {**part_dict,**mt_dict}
                    mt_df = mt_df.append(dict, ignore_index=True)
    #mt_df.to_excel(f'meeting.xlsx',sheet_name='meetings',index=False)
    mts_df = get_stats_df(mt_df)
    print(t.timeit())
    #df.to_excel(f'meeting.xlsx',sheet_name='meetings',index=False)
    #meetings_df = get_stats_df(list)
    mts_df.to_excel(f'meeting_stats_{param_dict["from"]}-{param_dict["to"]}.xlsx',sheet_name='meetings',index=False)

# execute main when called directly
if __name__ == '__main__':
    main()
