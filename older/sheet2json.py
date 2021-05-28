def sheet2json(sheet):
    #import json module to convert dict to json in the end
    import json
    #import pandas read_excel module to inject an excel into a DataFrame
    from pandas import read_excel
    # make sure we use the first sheet as source for our dataframe
    df = read_excel(sheet,sheet_name=0)
    d = {}
    # for every unique meeting collect all attendees in one list of dictionaries
    # with the needed key-value pairs
    for meeting in df['name_meeting'].unique():
        d[meeting] = [{
        'fn': df['fn_participant'][item],
        'sn': df['sn_participant'][item],
        'email': df['email_participant'][item]} 
        for item in df[df['name_meeting']==meeting].index]
    # convert dict in json
    d_json = json.dumps(d)
    #return json to be further processed
    return d_json

import excel2json
excel2json()