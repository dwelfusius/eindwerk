import string


def inv_tojson(sheet):
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

def inv_todict(sheet):
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
    #return dict to be further processed
    return d

def meet_todict(sheet):
    #import pandas read_excel module to inject an excel into a DataFrame
    import pandas
    from pandas import read_excel
    # make sure we use the first sheet as source for our dataframe
    df = read_excel(sheet,sheet_name=0)
    df.drop(columns=['fn_participant','sn_participant','email_participant'], index=[0], inplace=True)
    df.drop_duplicates(inplace=True)
    d = {}
    # for every unique meeting collect all attendees in one list of dictionaries
    # with the needed key-value pairs
    d = df.to_dict()
    #return dict to be further processed
    return d

'''
    for meeting in df['name_meeting'].unique():
        d[meeting] = [{
        'date_meeting': df['date_meeting'][item],
        'start': df['start_hour'][item],
        'end': df['end_hour'][item]} 
        for item in df[df['name_meeting']==meeting].index]
        '''