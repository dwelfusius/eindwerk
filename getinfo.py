import requests
import json

access_token = 'NjE2NTMwMDYtZmI1NS00NjIyLWJmZDUtYTk0OWM3NjI2MmU2NGNkNzM4NTQtZWM0_PF84_e4d4112d-2548-4a47-810e-04fe45ea181f'

url = 'https://webexapis.com/v1/organizations'
#url = "https://webexapis.com/v1/adminAudit/events"
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}

https://webexapis.com/v1/meetingParticipants?meetingId=560d7b784f5143e3be2fc3064a5c4999&hostEmail=john.andersen@example.com



payload = {
'orgId':'Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE',
'from': '2018-01-01T13:12:11.789Z',
'to': '2018-01-01T14:12:11.789Z',
'actorId' :'ZWUzNDNmYjEtNGQzNS00ZjNmLWE2ZDctMzZkNzVlYjk0ZWVm',
'max':100,
'offset':0}



payload= json.dumps(payload)
print(json.dumps(payload, indent=2))
res = requests.get(url, headers=headers, json=payload)
print(res.status_code)
