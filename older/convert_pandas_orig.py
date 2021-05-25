#import pandas modules for excel input and parsing
from pandas import read_excel,to_datetime,Timestamp

def excel_todict(sheet,tzone_str):
    #inject the first excel sheet into a DataFrame
    df = read_excel(sheet,sheet_name=0)
    #create DEEP copy of the df since we will modify it and don't want to change original
    inv_df = df.copy(deep=True)
    
    #this function will convert the
    def inv_todict(i):
        d = {}
        # for every unique meeting collect all attendees in one list of dictionaries
        # with the needed key-value pairs
        d = [{
        'displayname': inv_df['fn_participant'][item]+' '+inv_df['sn_participant'][item],
        'email': inv_df['email_participant'][item]}
        #  host?? 
        for item in inv_df[inv_df['name_meeting']==df['name_meeting'][i]].index]
        return d

    def parse_time(column):
        date = to_datetime(df['date_meeting']+' '+df[column+'_hour'])
        df[column] = date.apply(lambda d: Timestamp(d, tz = tzone_str).isoformat())

    def meet_todict():
        df.drop_duplicates(subset='name_meeting',inplace=True)
        d = {}
        
        parse_time('end')
        parse_time('start')

        for i in df.index:
            d[df['name_meeting'][i]] = {
            'title': df['name_meeting'][i],
            'start': df['start'][i],
            'end': df['end'][i],
            'timezone': tzone_str,
            'enabledAutoRecordMeeting': False,
            'allowAnyUserToBeCoHost': False,
            'invitees': inv_todict(i)
            }
        return d
    return meet_todict()
