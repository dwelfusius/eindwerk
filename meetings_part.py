from webexteamssdk import WebexTeamsAPI
import requests

from webexteamssdk.utils import json_dict

'''
url = "https://webexapis.com/v1/meetings?from=2021-05-01&to=2021-05-31&siteUrl=eindwerk.webex.com&hostEmail=eindwerk.automation@outlook.be"

payload={}
headers = {
  'Authorization': 'Bearer YjM1NTRlNDgtNmMxOC00MTFjLWIzN2QtNTExZmZjY2QyMzQwNmZiMzlhYjctYjRm_P0A1_8ffe788c-4bbf-4bd8-8adb-825c355cc81f'
}

response = requests.get(url, headers=headers, data=payload)

dict = json_dict(response.text)

for m in dict.values():
    meetingId = m[0]["id"]

    url = "https://webexapis.com/v1/meetingParticipants?meetingId="+ meetingId
    payload={}
    headers = {
    #'Authorization': 'Bearer ZjRmNWQ3YzItNDg0NC00ZmI1LWJlNzYtZjkwNTA5MTE0MGRiYjRkYzMxMzEtNjk0_P0A1_8ffe788c-4bbf-4bd8-8adb-825c355cc81f'
    'Authorization': 'Bearer YjM1NTRlNDgtNmMxOC00MTFjLWIzN2QtNTExZmZjY2QyMzQwNmZiMzlhYjctYjRm_P0A1_8ffe788c-4bbf-4bd8-8adb-825c355cc81f'
    }

    response = requests.get(url, headers=headers, data=payload)

    print(response.text)

'''


api = WebexTeamsAPI(access_token='YjM1NTRlNDgtNmMxOC00MTFjLWIzN2QtNTExZmZjY2QyMzQwNmZiMzlhYjctYjRm_P0A1_8ffe788c-4bbf-4bd8-8adb-825c355cc81f')


client_id = "<from oauth>"
client_secret = "<from oauth>"
oauth_code = "<from oauth>"
redirect_uri = "<from oauth>"
api = WebexTeamsAPI(client_id=client_id,
                    client_secret=client_secret,
                    oauth_code=oauth_code,
                    redirect_uri=redirect_uri
                    )
api.people.me()
#Person({"displayName": "Chris Lunsford", "firstName": "Chris", "created": "2012-06-15T20:36:48.914Z", "lastName": "Lunsford", "emails": ["chrlunsf@cisco.com"], "avatar": "https://1efa7a94ed216783e352-c62266528714497a17239ececf39e9e2.ssl.cf1.rackcdn.com/V1~ba1ecf557a7e0b7cc3081998df965aad~7-HrvYOJSQ6eJgWJuFVbzg==~1600", "id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mZjhlZTZmYi1hZmVmLTRhNGQtOTJiMS1kNmIyMTZiNTg5NDk"})

'''