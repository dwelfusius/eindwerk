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
        return dict["items"]
    else:
        print(response.status_code,response.url, response.reason)

def get_part_stats(m):
    part = (part_list(m.id))
    if type(part) is list:
        df = pd.DataFrame(part)["devices"]        
        mins = 0
        for i in df:
            left = pan_dt(i[0]['leftTime'])
            joined = pan_dt(i[0]['joinedTime'])
            mins += pd.Timedelta(left - joined).seconds / 60.0
        part_dict = {
        'Total_Participant_Min': int(mins),
        'Total_Participants': len(df)
            }
        #print('ok')
        return part_dict
    else:
        print('Nok part')
        return {}


def get_param(age_month):
    #date_d = delta(months=int('-'+str(age_month)))
    date_d = delta(days=-31)    
    date   = dt.today() + delta(days=+1)
    param_dict = {
        'to': date.strftime(format='%Y-%m-%d'),
        'from': (date + date_d).strftime(format='%Y-%m-%d'),
        'siteUrl': env['siteUrl'],
        'max': 100
    }
    #print('---4-- ok')
    return param_dict

def get_meeting(m):
    mt_dict = {
        'id': m.id,
        #'day' : dt.strftime(dt.strptime(m.start[0:10],'%Y-%m-%d'), format='%d/%m/%Y'),
        'day' : dt.strftime(m.start, format='%d/%m/%Y'),
        'start': m.start,
        'end': m.end, 
        'hostUserId': m.hostUserId
    }
    print('---5-- ok')
    return mt_dict

def get_stats_df(df):
    cp_df = df.copy(deep=True)
    cp_df.fillna(0, inplace=True, downcast='infer')
    for r in cp_df.iterrows():   
        for i in df:
            left = pan_dt(i[0]['leftTime'])
            joined = pan_dt(i[0]['joinedTime'])
            mins = mins + pd.Timedelta(left - joined).seconds / 60.00
        part_dict = {
            'Total_Participant_Min': mins,
            'Total_Participants': len(df)
        }
        part_df = part_df.append(part_dict, ignore_index=True, inplace=True)

    df = pd.DataFrame(list).result.fillna(0, inplace=True, downcast='infer')


def main():
    t = Timer()
    print(t.timeit())
    #people_list = pd.read_excel('people.xlsx')['people'].tolist()
    url = "https://webexapis.com/v1/"
    people_list  = get_emails(pages_list(f'{url}people'))
    print(t.timeit())
    param_dict = get_param(age_month=3)
    print(t.timeit())
    mt_df = pd.DataFrame()
    for person in people_list:
        param_dict['hostEmail'] = person
        uri = f"{url}meetings?{urlencode(param_dict)}"
        pages = pages_list(uri)
        for page in pages:
            df = pd.DataFrame(page["items"])
            for mt in df.iterrows():
                tm.sleep(2)
                mt_row = mt[1]
                mt_dict = get_meeting(mt_row)
                part_dict = get_part_stats(mt_row)
                dict = {**part_dict,**mt_dict}
                mt_df = mt_df.append(dict, ignore_index=True)
    print(t.timeit())
    mt_df.to_excel(f'meeting.xlsx',sheet_name='meetings',index=False)
    mts_df = get_stats_df(mt_df)
    print(t.timeit())
    df.to_excel(f'meeting.xlsx',sheet_name='meetings',index=False)
    #meetings_df = get_stats_df(list)
    #meetings_df.to_excel(f'meeting_stats_{param_dict["from"]}-{param_dict["to"]}.xlsx',sheet_name='meetings',index=False)

# execute main when called directly
if __name__ == '__main__':
    main()
