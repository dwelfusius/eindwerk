import requests
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder

access_token = 'OGJhOWUyZWYtZmJlMy00ZmRjLTlkYTktOTQzNjdiZmQ1MjAzZDBjNWQ4YzgtOTE5_PE93_2ed27726-ce04-44f4-bcaf-285686073cf8'
url = 'https://webexapis.com/v1/messages'
room_id = 'Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vOWUyYWY5ZDAtYTJlMS0xMWViLWJhNTUtMzk2NTcxMDFkNjlm'

headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}

messages = ['https://github.com/dwelfusius/Devasc_Skills.git','Here are my screenshots of netacad-devasc skills-based exam:']
for m in messages:
    params = {'roomId': room_id, 'markdown': m}
    res = requests.post(url, headers=headers, json=params)

base = 'screenshots/'
files = os.listdir(base)
for file in files:
    path = base+file
    m = MultipartEncoder({'roomId': room_id,
                        'text': f'{file} attached',
                        'files': (path, open(path, 'rb'),
                        'image/png')})
    r = requests.post(url, data=m,
                    headers={'Authorization': 'Bearer {}'.format(access_token),'Content-Type': m.content_type})
    print(r.status_code)