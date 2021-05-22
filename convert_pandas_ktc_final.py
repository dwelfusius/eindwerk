from timeit import Timer
from pandas import read_excel,to_datetime,Timestamp
tzone_str = 'Europe/Brussels'
sheet = 'list_webex.xlsx'

def parse_time(column, df):
    date = to_datetime(df['date_meeting']+' '+df[column+'_hour'])
    return date.apply(lambda d: Timestamp(d, tz = tzone_str).isoformat())

def transform_df(df, date_col):
    cp_df = df.copy(deep=True)
    for c in date_col:
        cp_df[c] = parse_time(c, cp_df)
    cp_df['displayname'] = cp_df['fn_participant']+' '+cp_df['sn_participant']
    cp_df.drop(columns=['start_hour','end_hour','date_meeting','fn_participant','sn_participant'],inplace=True)
    return cp_df


def main():
    t = Timer()
    #read excel file
    df = read_excel('list_webex.xlsx',sheet_name=0)
    df = transform_df(df, ['end','start'])
    d = {}
    # loop through a unique meeting list created from the df object
    for name in df['name_meeting'].unique():
        #create a subset containing only the rows belonging to this meeting
        sub_df = df[df['name_meeting']==name]
        #put the values of the first subset tuple in a pandas frame
        mt = next(sub_df.itertuples())
        #per unique meeting create one dictionary object
        d[name] = {
        'title': mt.name_meeting,
        'start': mt.start,
        'end'  : mt.end,
        'timezone': tzone_str,
        'enabledAutoRecordMeeting': False,
        'allowAnyUserToBeCoHost': False,
        'invitees': [{ 
            'displayname': i.displayname,
            'email': i.email_participant
            }
        # per meeting collect all attendees in one list of dictionaries 
        for i in sub_df.itertuples()]}
    print(t.timeit())
    return d

# execute main when called directly
if __name__ == '__main__':
    main()