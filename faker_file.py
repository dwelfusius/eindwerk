import pandas as pd
sheet = 'list_webex.xlsx'
from faker import Faker
fake = Faker()
Faker.seed(0)

orig_df = pd.read_excel(sheet,sheet_name=0)
l = []
for c in list(range(0,30)):
    nums = list(range(1,12))
    for n in nums: 
        d = {}
        d['name_meeting'] = 'test_meeting' + n.__str__()
        d['date_meeting'] = '20/'+n.__str__()+'/2021'
        d['start_hour']   = '19:00'
        d['end_hour']     = '21:00'
        d['fn_participant']   = fake.first_name()
        d['sn_participant']    = fake.last_name()
        d['email_participant'] = fake.email()
        l.append(d)
new = pd.DataFrame(l)
#new = orig_df.append(l, ignore_index=True)
new.to_excel('new.xlsx')
