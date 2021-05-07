import requests
access_token = 'M2IwMTE1MTQtYWJiOS00MTBjLWE5YjYtZWI4M2JmZWQxOTZkNDFlMmJhYTctOWVi_PE93_2ed27726-ce04-44f4-bcaf-285686073cf8'

ids = ["Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vMWQ2ZWUwZTAtYTIxOS0xMWViLWE2YmEtYjdiZGM5ZjgyMDc2", 
"Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vMGZjOTYwZjAtYTIxOS0xMWViLTkyMDEtMjU0NjA2ZjI0ZDQ5",
"Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vOWI0NDZlMDAtYTIxOC0xMWViLTljMDItOGJiY2VmM2RlNmQ1",
"Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vN2ZkMDNiNDAtYTIxOC0xMWViLWI1OWQtMDVkZjFiNWRhNzdk",
"Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vNDI2ZmE5OTAtYTIxMS0xMWViLTk3Y2EtOGI3OGI4MWJjMzZl"]


for room_id in ids:
    url = f'https://webexapis.com/v1/rooms/{room_id}'
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }
    res = requests.delete(url, headers=headers)
'''

room_id = "Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vMTNmOTY1MjAtYTIxMC0xMWViLTg1YjMtYjdjNDM2ODY3NmVm"
url = f'https://webexapis.com/v1/rooms/{room_id}'
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}
res = requests.delete(url, headers=headers)
'''