import json
from pandas import read_excel
df = read_excel('list_webex.xlsx',sheet_name=0)
d = {}
for room in df['name_room'].unique():
    d[room] = [{
    'fn': df['fn_participant'][item],
    'sn': df['sn_participant'][item],
    'email': df['email_participant'][item]} 
    for item in df[df['name_room']==room].index]

d_json = json.dumps(d)
print(d_json)
'''
d = df.groupby('name_room')[[
    'fn_participant','sn_participant','email_participant'
    ]].apply(lambda g: g.values.tolist()).to_dict()'''


d_json = json.dumps(d)
print(d_json)