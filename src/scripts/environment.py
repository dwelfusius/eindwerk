""" This file contains the bearer tokens and other information
used in testing the scripts. You can think of it as a postman
environment. It's NOT recommended to put production data into
this file. Especially no tokens.
"""


#biasc
biasc_token = 'ZjVlOGU3NzgtY2JlOC00NTMyLWI2MWUtNGQ3YjEwNjgzMjNjY2ZjODU4NDktODYz_PF84_e4d4112d-2548-4a47-810e-04fe45ea181f'
biasc = {
'token' : biasc_token,
'hostEmail' : 'yvan.rooseleer@biasc.be',
'siteUrl': 'biasc.webex.com',
'headers' : {
    'Authorization': f'Bearer {biasc_token}'
}}


#integration with admin
admin_token = 'OWJmZDFlYWUtM2JiNS00Njg3LTg1N2MtMDAwZmMxMTc3ZTM1Zjg5YmNkNzktMmEz_P0A1_8ffe788c-4bbf-4bd8-8adb-825c355cc81f'
int_report ={
'token' : admin_token,
'hostEmail' : 'eindwerk.automation@outlook.be',
'siteUrl': 'eindwerk.webex.com',
'headers' : {
    'Authorization': f'Bearer {admin_token}'
}}

#integration with automation
aut_token = 'MzY5MDE3N2QtZGYzNC00MWJkLWIxMmItNjhlNjk2YmU1YzJhNWZlMjE3Y2UtYjVk_P0A1_8ffe788c-4bbf-4bd8-8adb-825c355cc81f'
int_automation ={
'token' : aut_token,
'siteUrl': 'eindwerk.webex.com',
'hostEmail' : 'eindwerk.automation@outlook.be',
'headers' : {
    'Authorization': f'Bearer {aut_token}'
}
}



#eindwerk_automation
aut = 'MmQ5Y2M4ODAtZWJkNi00MDNjLWFiYWMtYjBiMDdiZjRjNTZkN2FlYzBjN2EtN2Jm_P0A1_8ffe788c-4bbf-4bd8-8adb-825c355cc81f'
#eindwerk admin
adm = 'NDU3ZGE5ZTEtODhlOC00YmJmLWI3ZGEtMDU5ZDg5MDdlM2ZiZjM4OWJjMTYtZTJm_P0A1_8ffe788c-4bbf-4bd8-8adb-825c355cc81f'
