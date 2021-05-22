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


def main():
    #read excel file
    df = read_excel(sheet,sheet_name=0)
    meet_df = df.copy()
    # merge dataframes to final dict
    meet_df.drop_duplicates(subset='name_meeting',inplace=True)
    d = {}
    #    
    meet_df['end'] = parse_time('end', df)
    meet_df['start'] = parse_time('start', df)
    
    # merge dataframes to final dict
    for r in meet_df.index:
        print(meet_df['name_meeting'][r])
        d[meet_df['name_meeting'][r]] = {
        'title': meet_df['name_meeting'][r],
        'start': meet_df['start'][r],
        'end': meet_df['end'][r],
        'timezone': tzone_str,
        'enabledAutoRecordMeeting': False,
        'allowAnyUserToBeCoHost': False,
        'invitees': inv_select(r, df)
        }
    print(d)
    return d

# execute main when called directly
if __name__ == '__main__':
    main()