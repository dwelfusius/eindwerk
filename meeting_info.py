import requests
import json
from environment import biasc as env
#from environment import int_report as env
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta as delta
import pandas as pd

access_token = env['token']
headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

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


def list_people():
    url = "https://webexapis.com/v1/people" 
    first_page = requests.get(url,headers=headers)
    yield first_page.json()
    if 'next' in first_page.links:
        page = first_page.links['next']['url']
        while page:
            next_page = requests.get(page,headers=headers)
            yield next_page.json()
            if 'next' in next_page.links:
                page = next_page.links['next']['url']
            else:
                page = False


def count_part(meetingId):
    url = f"https://webexapis.com/v1/meetingParticipants?meetingId={meetingId}"
    response = requests.get(url, headers=headers, data={})
    if response.status_code==200:
        dict = json.loads(response.text)
        return (len(dict["items"]))

def main():
    #people_list = pd.read_excel('people.xlsx')['people'].tolist()
    people_list = get_emails(list_people())
    url_meetings = "https://webexapis.com/v1/meetings"
    #delta = delta(months=-3)
    v_delta = delta(days=-10)
    date = dt.today() + delta(days=+1)
    date_to = date.strftime(format='%Y-%m-%d')
    date_from = (date + v_delta).strftime(format='%Y-%m-%d')
    siteUrl = env['siteUrl']
    mt_list = []
    for p in people_list:
        hostEmail= p
        uri = f"{url_meetings}?from={date_from}&to={date_to}&siteUrl={siteUrl}&hostEmail={hostEmail}"
        response = requests.get(uri, headers=headers)
        if response.status_code==200:
            meetings_json = response.json()
            for m in meetings_json['items']:
                meetingId = m["id"]
                mt_dict = {
                    'id': meetingId,
                    'meetingNumber': m['meetingNumber'], 
                    'timezone': m['timezone'], 
                    'start': m['start'],
                    'end': m['end'], 
                    'hostUserId': m['hostUserId'],
                    'participants': count_part(meetingId)
                }
                mt_list.append(mt_dict)
    df = pd.DataFrame(mt_list)
    #df.to_excel(f'meeting.xlsx',sheet_name='meetings',index=False)
    df.to_excel(f'meeting_stats_{date_from}-{date_to}.xlsx',sheet_name='meetings',index=False)

# execute main when called directly
if __name__ == '__main__':
    main()
