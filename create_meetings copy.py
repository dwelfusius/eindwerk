from convert import excel_todict
data_dict = excel_todict('list_webex.xlsx','Europe/Brussels')

import requests
import json

access_token = 'NmVjMGNkODYtMDRiZi00NTExLWIwZjEtMzI4ZGM2MmZkMTdmOTQzYmZlM2QtMDU0_PE93_2ed27726-ce04-44f4-bcaf-285686073cf8'


url = "https://webexapis.com/v1/meetings"
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}


for m in data_dict.items():
    payload= json.dumps(m[1])
    print(json.dumps(payload, indent=2))
    #res = requests.post(url, headers=headers, json=payload)
    #print(res.status_code)
'''




dict = json.loads(data_dict)
for m in dict:
    payload = json.dumps(dict[m])
    #print(json.dumps(payload, indent=4))
    res = requests.post(url, headers=headers, json=payload)
    print(res.status_code)
'''