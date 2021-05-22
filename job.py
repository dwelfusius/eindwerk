from sheet2json import sheet2json
json = sheet2json('list_webex.xlsx')
print(json)



import faker

e = faker()

e.seed(0)
for _ in range(60):
    e.first_name_nonbinary()