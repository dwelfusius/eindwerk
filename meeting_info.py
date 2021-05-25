import webexteamssdk as wx


import requests


wx.init

url = "https://webexapis.com/v1/meetings?from=2021-05-01&to=2021-05-31&siteUrl=biasc.webex.com&hostEmail=yvan.rooseleer@biasc.be"

payload={}
headers = {
    'Authorization': 'Bearer YTA1ZWE4ODktN2FkYS00MDJkLTgxM2QtYTc2NjgyOWExMGJjMjU0ZTRkNDEtMmQ0_PF84_e4d4112d-2548-4a47-810e-04fe45ea181f'
}

response = requests.get(url, headers=headers, data=payload)

print(response.text)
