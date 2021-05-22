from timeit import Timer

import json
from collections import OrderedDict
import numpy as np
from itertools import islice
import openpyxl as px
from datetime import datetime as dt
from backports.zoneinfo import ZoneInfo as zi
t = Timer()
# Open the workbook and select a worksheet
wb = px.load_workbook('list_webex.xlsx')
sheet = wb['list_webex']
tzone_str = 'Europe/Brussels'

def parse_time(column, do):
    d = do['date_meeting']+' '+do[column+'_hour']+':00'
    date = dt.strptime(d, '%d/%m/%Y %H:%M:%S').replace(tzinfo=zi(tzone_str))
    date.replace(tzinfo=zi(tzone_str)).isoformat()
    return date.isoformat()


# List to hold dictionaries
meeting_list = []
# Iterate through each row in worksheet and fetch values into tuples
for row in islice(sheet.values, 1, sheet.max_row):
    meeting_list.append(row)


headers = []
for i in sheet.iter_cols():
    headers.append(i[0].value)

meeting_dictlist = []
for i in meeting_list:
    
    d = {}
    d[headers[0]] = i[0]
    d[headers[1]] = i[1]
    d[headers[2]] = i[2]
    d[headers[3]] = i[3]
    d[headers[4]] = i[4]
    d[headers[5]] = i[5]
    d[headers[6]] = i[6]
    meeting_dictlist.append(d)

#Create a set of unique meeting
unimeeting_list = []
for meeting in meeting_list:
    if not unimeeting_list.__contains__(meeting[0]):
        unimeeting_list.append(meeting[0])

# Create list to collect information to convert to json
treemeetings_dict = {}
for title in unimeeting_list:
    meeting = meeting_dictlist['name_meeting'==title]
    members_list = []
    # Run through participants list and create a dict object per member
    for item in meeting_dictlist:
        if title == item['name_meeting']:
            member = OrderedDict()
            member['displayname'] = item['fn_participant']+' '+item['sn_participant']
            member['email'] = item['email_participant']
            # Add dict object to members list
            members_list.append(member)
    # Create dict object with meeting name + aggregated members list
    treemeeting_dict = {}
    treemeeting_dict['title'] = title
    treemeeting_dict['start'] = parse_time('start', meeting)
    treemeeting_dict['end'] = parse_time('end', meeting)
    treemeeting_dict['timezone'] = tzone_str
    treemeeting_dict['enabledAutoRecordMeeting'] = False
    treemeeting_dict['allowAnyUserToBeCoHost'] = False
    treemeeting_dict['invitees'] = members_list
    # Add one meeting dict object to final dataset
    treemeetings_dict[title] = treemeeting_dict

# Serialize the list of dicts to JSON
d = treemeetings_dict
print(t.timeit())

