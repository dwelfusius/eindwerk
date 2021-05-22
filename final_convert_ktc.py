from pandas import read_excel,to_datetime,Timestamp
sheet = 'list_webex.xlsx'
tzone_str = 'Europe/Brussels'

def parse_time(column, df):
    date = to_datetime(df['date_meeting']+' '+df[column+'_hour'])
    return date.apply(lambda d: Timestamp(d, tz = tzone_str).isoformat())

def inv_select(p_meeting_name, df):
    #create DEEP copy of the df since we will modify it and don't want to change original
    inv_df = df.copy(deep=True)
    # per meeting collect all attendees in one list of dictionaries
    inv = [{
    'displayname': inv_df['fn_participant'][item]+' '+inv_df['sn_participant'][item],
    'email': inv_df['email_participant'][item]}
    #  host?? 
    for item in inv_df[inv_df['name_meeting']==df['name_meeting'][p_meeting_name]].index]
    return inv

def transform_df(df, date_col):
    d = df.copy(deep=True)
    d.drop_duplicates(subset='name_meeting',inplace=True)
    for t in date_col:
        d[t] = parse_time(t, d)
    return d

def main():
    #read excel file
    orig_df = read_excel(sheet,sheet_name=0)
    meet_df = transform_df(orig_df, ['end','start'])
    
    d = {}
    # merge dataframes to final dict
    for r in meet_df.index:
        d[meet_df['name_meeting'][r]] = {
        'title': meet_df['name_meeting'][r],
        'start': meet_df['start'][r],
        'end': meet_df['end'][r],
        'timezone': tzone_str,
        'enabledAutoRecordMeeting': False,
        'allowAnyUserToBeCoHost': False,
        'invitees': inv_select(r, orig_df)
        }
    print(d)
    return d

# execute main when called directly
if __name__ == '__main__':
    main()