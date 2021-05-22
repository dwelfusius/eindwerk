from timeit import Timer
from pandas import read_excel,to_datetime,Timestamp
tzone_str = 'Europe/Brussels'
sheet = 'list_webex.xlsx'

def parse_time(cols, df):
    col_list = []
    for c in cols:
        date = to_datetime(df['date_meeting']+' '+df[c+'_hour'])
        col_list.append(date.apply(lambda d: Timestamp(d, tz = tzone_str).isoformat()))
    return col_list

def inv_select(df):
    inv_dic = {}
    # per meeting collect all attendees in one list of dictionaries
    for meeting in df['name_meeting'].unique():
        inv_dic[meeting] = [{
        'displayname': item.fn_participant+' '+item.sn_participant,
        'email': item.email_participant} 
        for item in df[df['name_meeting']==meeting].itertuples()]    

    return inv_dic

def main():
    t = Timer()
    #read excel file to panda dataframe
    df = read_excel('list_webex.xlsx',sheet_name=0)
        #transform date and time to iso dates
    df['end'],df['start'] = parse_time(['end','start'], df)
    inv_dict = inv_select(df)
    d = {}
    # loop through a unique meeting list created from the df object
    for name in df['name_meeting'].unique():
        #create a subset containing only the rows linked to this meeting
        for mt in df[df['name_meeting']==name].itertuples():
            #per unique meeting create one dictionary object
            d[mt.name_meeting] = {
            'title': mt.name_meeting,
            'start': mt.start,
            'end'  : mt.end,
            'timezone': tzone_str,
            'enabledAutoRecordMeeting': False,
            'allowAnyUserToBeCoHost': False,
            # per meeting collect all attendees in one list of dictionaries
            'invitees': inv_dict[mt.name_meeting]}     
    print(t.timeit())
    return d

# execute main when called directly
if __name__ == '__main__':
    main()

