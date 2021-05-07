def sheet2json(sheet):
    import json
    from pandas import read_excel
    df = read_excel(sheet,sheet_name=0)
    d = {}
    for room in df['name_room'].unique():
        d[room] = [{
        'fn': df['fn_participant'][item],
        'sn': df['sn_participant'][item],
        'email': df['email_participant'][item]} 
        for item in df[df['name_room']==room].index]
    d_json = json.dumps(d)
    return d_json