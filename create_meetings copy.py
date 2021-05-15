from convert import meet_todict
data_dict = meet_todict('list_webex.xlsx')
import requests
import json

from datetime import datetime

access_token = 'YmM2MzkwNTMtMDUxZi00NmE0LTg5YzQtMDVlZDI0MWJjMzkwMjA1NTI5NWItOTRh_PE93_2ed27726-ce04-44f4-bcaf-285686073cf8'

url = "https://webexapis.com/v1//meetings"
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}




for m in data_dict.items():
    my_date = datetime(date=m[1][0]['date'])
    print(my_date.isoformat())
    #payload="{\n    \"title\": \"Sample Title\",\n    \"agenda\": \"Sample Agenda\",\n    \"password\": \"A@ssword123\",\n    \"start\": \"2021-05-15T14:00:00+02:00\",\n    \"end\": \"2021-05-15T14:30:00+02:00\",\n    \"timezone\": \"Europe/Brussels\", \n    \"enabledAutoRecordMeeting\": false,\n    \"allowAnyUserToBeCoHost\": false\n}"
    #res = requests.post(url, headers=headers, json=payload)
    #print(res.status_code)

'''
room_id = res.json().get('id')
if room_id:
    person_email = 'alain.pieters@biasc.be'
    url = 'https://webexapis.com/v1/memberships'
    params = {'roomId': room_id, 'personEmail': person_email}
    res = requests.post(url, headers=headers, json=params)
    print(json.dumps(res.json(), indent = 4))
print(room_id)




payload="{\n    \"title\": \"Sample Title\",\n    \"agenda\": \"Sample Agenda\",\n    \"password\": \"A@ssword123\",\n    \"start\": \"2021-05-15T14:00:00+02:00\",\n    \"end\": \"2021-05-15T14:30:00+02:00\",\n    \"timezone\": \"Europe/Brussels\", \n    \"enabledAutoRecordMeeting\": false,\n    \"allowAnyUserToBeCoHost\": false\n}"


response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
'''