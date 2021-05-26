import pandas as pd
from faker import Faker
import random

fake = Faker()
Faker.seed(0)

hostList = ["False"] * 14 + ["True"]
hostEmaillist = ["eindwerk.user1@outlook.be","eindwerk.user2@outlook.be","eindwerk.user3@outlook.be"]

l = []
nums = list(range(1,12))
for n in nums: 
    date = fake.date_between(start_date='today', end_date='+10d')
    title = n.__str__()
    for c in list(range(0,32)):
        host = random.choice(hostList)
        d = {}
        d['name_meeting'] = 'test_meeting' + title
        d['date_meeting'] = date.strftime(fmt='%d/%m/%Y')
        d['start_hour']   = '19:00'
        d['end_hour']     = '21:00'
        d['fn_participant']   = fake.first_name()
        d['sn_participant']    = fake.last_name()
        if host=="True":
            d['email_participant'] = random.choice(hostEmaillist)
        else:
            d['email_participant'] = fake.email()
        d['host'] = host
        l.append(d)
new = pd.DataFrame(l)
new.to_excel('list_webex.xlsx',sheet_name='list_webex',index=False)
