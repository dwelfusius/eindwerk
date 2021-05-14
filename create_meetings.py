from webexteamssdk import WebexTeamsAPI
#from webexteamssdk.environment import WEBEX_TEAMS_ACCESS_TOKEN
'''
from sheet2json import sheet2json
json = sheet2json('list_webex.xlsx')
'''

api = WebexTeamsAPI()
list = api.people.me()
print(list)