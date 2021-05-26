from environment import biasc as env
import requests
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta as delta
import json

access_token = env['token']
url = "https://webexapis.com/v1/meetings"

date = dt.today() + delta(days=+1)
delta = delta(months=-3)
date_to = date.strftime(format='%Y-%m-%d')
date_from = (date + delta).strftime(format='%Y-%m-%d')
siteUrl= env['siteUrl']
hostEmail= env['hostEmail']

headers = {
  'Authorization': 'Bearer {}'.format(access_token)
}
uri = f"{url}?from={date_from}&to={date_to}&siteUrl={siteUrl}&hostEmail={hostEmail}"
response = requests.get(uri, headers=headers, data={})


mts_dict = json.loads(response.text)

mt_list = []
for m in mts_dict.values():
    meetingId = m[0]["id"]
    url = "https://webexapis.com/v1/meetingParticipants?meetingId="+ meetingId
    payload={}
    response = requests.get(url, headers=headers, data=payload)
    dict = json.loads(response.text)
    mt_list.append(dict)

print(mt_list)