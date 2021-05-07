import requests
import json
access_token = 'M2IwMTE1MTQtYWJiOS00MTBjLWE5YjYtZWI4M2JmZWQxOTZkNDFlMmJhYTctOWVi_PE93_2ed27726-ce04-44f4-bcaf-285686073cf8'

url = 'https://webexapis.com/v1/rooms'
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}
params={'title': 'netacad_devasc_skills_KC'}
res = requests.post(url, headers=headers, json=params)
print(res.status_code)

room_id = res.json().get('id')
if room_id:
    person_email = 'alain.pieters@biasc.be'
    url = 'https://webexapis.com/v1/memberships'
    params = {'roomId': room_id, 'personEmail': person_email}
    res = requests.post(url, headers=headers, json=params)
    print(json.dumps(res.json(), indent = 4))
print(room_id)