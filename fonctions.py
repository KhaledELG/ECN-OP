#TODO : créer une fonction main, GetID, GetToken, GetRequest et gerer les demandes à faire 

import requests
import json

# Defines the function to intercept a token
def GetToken(Client_ID):
    authURL = 'https://id.twitch.tv/oauth2/token'
    Secret  = "byddoub52je363dea4ntqnueqs4qlu"
    AutParams = {'client_id': Client_ID,
                'client_secret': Secret,
                'grant_type': 'client_credentials',
                'scope': "channel_subscriptions channel_read user_read"
                }
    AutCall = requests.post(url=authURL, params=AutParams) 
    access_token = AutCall.json()['access_token']
    return access_token

# Defines the function to send a request
def GetRequest(URL,head):
    r = requests.get(URL, headers = head).json()['data']
    return r

# Defines the function to collect the streamer id
def GetID(Client_ID, access_token, streamer_name):
    URL = "https://api.twitch.tv/helix/users?login="+streamer_name
    head = {
    'Client-ID' : Client_ID,
    'Authorization' :  "Bearer " + access_token
    }
    return GetRequest(URL,head)[0]["id"]

# Defines the function to collect the list of top games
def GetTopGames(Client_ID, access_token):
    URL = "https://api.twitch.tv/helix/games/top"
    head = {
    'Client-ID' : Client_ID,
    'Authorization' :  "Bearer " + access_token
    }
    x = GetRequest(URL,head)
    #print(json.dumps(x, indent=4, sort_keys=True))
    return x

def GetChannelIcalendar(Client_ID, access_token, broadcaster_id):
    URL = "https://api.twitch.tv/helix/schedule/icalendar?broadcaster_id="+broadcaster_id
    head = {
    'Client-ID' : Client_ID,
    'Authorization' :  "Bearer " + access_token
    }
    x = requests.get(URL, headers = head)
    return x #return un fichier .pyc ??

# def GetFollowedStreams(Client_ID, access_token, user_id):
#     URL = "https://api.twitch.tv/helix/streams/followed?user_id="+user_id
#     head = {
#     'Client-ID' : Client_ID,
#     'Authorization' :  "Bearer " + access_token
#     }
#     x = requests.get(URL, headers = head)
#     #print(json.dumps(x, indent=4, sort_keys=True))
#     #print(x)
#     #return x
# PROBLEME : POUR LES STREAMERS

# def GetBroadcasterSubscriptions(Client_ID, access_token, broadcaster_id):
#     URL = "https://api.twitch.tv/helix/subscriptions?broadcaster_id="+broadcaster_id
#     head = {
#     'Client-ID' : Client_ID,
#     'Authorization' :  "Bearer " + access_token
#     }
#     x = requests.get(URL, headers = head).json()
#     print(json.dumps(x, indent=4, sort_keys=True))
#     #return x
# PROBLEME : POUR LES STREAMERS

def GetVideos(Client_ID, access_token, broadcaster_id):
    URL = "https://api.twitch.tv/helix/videos?broadcaster_id="+broadcaster_id
    head = {
    'Client-ID' : Client_ID,
    'Authorization' :  "Bearer " + access_token
    }
    x = requests.get(URL, headers = head).json()
    print(x)
    #return x


