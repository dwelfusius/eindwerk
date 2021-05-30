import requests
import json
#from environment import biasc as env
from environment import int_report as env
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta as delta
import pandas as pd
from urllib.parse import urlencode

def get_emails_excel(emails):
    df = pd.DataFrame()
    df['people'].append(emails)
    df.to_excel(f'people.xlsx',sheet_name='people',index=False)


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
        print(f_page.reason)

def count_part(meetingId):
    url = f"https://webexapis.com/v1/meetingParticipants?meetingId={meetingId}"
    response = requests.get(url, headers=env['headers'])
    if response.status_code==200:
        dict = json.loads(response.text)
        return (len(dict["items"]))

def get_param(age_month):
    date_d = delta(months=int('-'+str(age_month)))
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
    'id': m["id"],
    'meetingNumber': m['meetingNumber'], 
    'timezone': m['timezone'], 
    'start': m['start'],
    'end': m['end'], 
    'hostUserId': m['hostUserId'],
    'participants': count_part(m["id"])
    }
    return mt_dict

def main():
    #people_list = pd.read_excel('people.xlsx')['people'].tolist()
    url = "https://webexapis.com/v1/"
    people_list  = get_emails(pages_list(f'{url}people'))
    param_dict = get_param(age_month=1)
    mt_list    = []
    for person in people_list:
        param_dict['hostEmail'] = person
        uri = f"{url}meetings?{urlencode(param_dict)}"
        #response = requests.get(url+'meetings', headers=headers, params=param_dict)
        pages = pages_list(uri)
        for page in pages:
            for mt in page["items"]:
                mt_list.append(get_meeting(mt))
    meetings_df = pd.DataFrame(mt_list).result.fillna(0, inplace=True, downcast='infer')
    #df.to_excel(f'meeting.xlsx',sheet_name='meetings',index=False)
    meetings_df.to_excel(f'meeting_stats_{param_dict["from"]}-{param_dict["to"]}.xlsx',sheet_name='meetings',index=False)

# execute main when called directly
if __name__ == '__main__':
    main()
