import requests
import json
from environment import biasc as env
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta as delta

url_people = "https://webexapis.com/v1/people"
access_token = env['token']
payload={}

headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}
response = requests.request("GET", url_people, headers=headers, data=payload)
people_json = response.json()
people_list = []
for p in people_json['items']:
    people_list.append(p['emails'][0])

url_meetings = "https://webexapis.com/v1/meetings"
date = dt.today() + delta(days=+1)
delta = delta(months=-3)
date_to = date.strftime(format='%Y-%m-%d')
date_from = (date + delta).strftime(format='%Y-%m-%d')
siteUrl= env['siteUrl']
for p in people_list:
    hostEmail= p
    uri = f"{url_meetings}?from={date_from}&to={date_to}&siteUrl={siteUrl}&hostEmail={hostEmail}"
    response = requests.get(uri, headers=headers, data={})
    meetings_json = response.json()
    for m in meetings_json['items']:
        print(m)