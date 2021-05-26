from convert_pandas import main as pd_main
from convert_nopandas import main as py_main
import requests
import json
from environment import int_automation as env
data_dict = pd_main()
#data_dict = py_main()

access_token = env['token']


url = "https://webexapis.com/v1/meetings"
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}

for m in data_dict.items():
    payload= json.dumps(m[1])
    res = requests.post(url, headers=headers, json=payload)
    print(res.status_code)

