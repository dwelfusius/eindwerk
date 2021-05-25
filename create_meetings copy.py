from convert_pandas_final_s import main as pd_main
from convert_nopandas import main as py_main

#data_dict = pd_main()
data_dict = py_main()


import requests
import json

#biasc
#access_token = 'MDFlZDg3MWEtNGFhNy00NmUzLWFkNmItNjIwNTM0MWUyMmJkNWVhMTgyNDQtMTRi_PF84_e4d4112d-2548-4a47-810e-04fe45ea181f'
#katrien
#access_token = 'YTI5Mjk2N2YtODZkOS00MTMxLWI3ZjUtMjlhYWE5NGZjODZjODhmNTg1OTYtOWRk_PE93_2ed27726-ce04-44f4-bcaf-285686073cf8'

#eindwerk_automation
#access_token = 'MmQ5Y2M4ODAtZWJkNi00MDNjLWFiYWMtYjBiMDdiZjRjNTZkN2FlYzBjN2EtN2Jm_P0A1_8ffe788c-4bbf-4bd8-8adb-825c355cc81f'
#eindwerk admin
access_token = 'NDU3ZGE5ZTEtODhlOC00YmJmLWI3ZGEtMDU5ZDg5MDdlM2ZiZjM4OWJjMTYtZTJm_P0A1_8ffe788c-4bbf-4bd8-8adb-825c355cc81f'

url = "https://webexapis.com/v1/meetings"
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}


for m in data_dict.items():
    payload= json.dumps(m[1])
 #   print(payload)
    #print(json.dumps(payload, indent=2))
    res = requests.post(url, headers=headers, json=payload)
    print(res.status_code)

