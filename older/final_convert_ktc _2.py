from pandas import read_excel,to_datetime,Timestamp
import json
sheet = 'list_webex.xlsx'
tzone_str = 'Europe/Brussels'

def parse_time(column, df):
    date = to_datetime(df['date_meeting']+' '+df[column+'_hour'])
    return date.apply(lambda d: Timestamp(d, tz = tzone_str).isoformat())

def inv_select(df):
    #create DEEP copy of the df since we will modify it and don't want to change original
    inv_dic = {}
    # per meeting collect all attendees in one list of dictionaries
    for meeting in df['name_meeting'].unique():
        inv_dic[meeting] = [{
        'displayname': df['fn_participant'][item]+' '+df['sn_participant'][item],
        'email': df['email_participant'][item]} 
        for item in df[df['name_meeting']==meeting].index]
    return inv_dic

def transform_df(df, date_col):
    d = df.copy(deep=True)
    d.drop_duplicates(subset='name_meeting',inplace=True)
    ##kan er makkelijk uit indien cross contamination
    for t in date_col:
        d[t] = parse_time(t, d)
    return d

def main():
    #read excel file
    orig_df = read_excel(sheet,sheet_name=0)
    meet_df = transform_df(orig_df, ['end','start'])
    inv_dict = inv_select(orig_df)

    d = {}
    # merge dataframes to final dict
    for r in meet_df.index:
        meeting = meet_df['name_meeting'][r]
        d[meet_df['name_meeting'][r]] = {
        'title': meet_df['name_meeting'][r],
        'start': meet_df['start'][r],
        'end': meet_df['end'][r],
        'timezone': tzone_str,
        'enabledAutoRecordMeeting': False,
        'allowAnyUserToBeCoHost': False,
        'invitees': inv_dict[meeting]
        }
    print(json.dumps(d))
    return d

# execute main when called directly
if __name__ == '__main__':
    main()