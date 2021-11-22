#################################################################################################

import requests
import json
import pandas as pd
import config

#################################################################################################

# Defines the function to intercept a token
def GetToken(Client_ID):
    authURL = 'https://id.twitch.tv/oauth2/token'
    Secret  = config.Secret
    AutParams = {'client_id': Client_ID,
                'client_secret': Secret,
                'grant_type': 'client_credentials',
                'scope': "channel:read:subscriptions"
                }
    AutCall = requests.post(url=authURL, params=AutParams) 
    access_token = AutCall.json()['access_token']
    return access_token

#################################################################################################

# Defines the function to collect the streamer id
def GetID(Client_ID, access_token, streamer_name):
    URL = "https://api.twitch.tv/helix/users?login="+streamer_name
    head = {
    'Client-ID' : Client_ID,
    'Authorization' :  "Bearer " + access_token
    }
    return requests.get(URL, headers = head).json()['data'][0]["id"]

#################################################################################################

# Defines the function to collect the list of top games
def GetTopGames(Client_ID, access_token):
    URL = "https://api.twitch.tv/helix/games/top"
    head = {
    'Client-ID' : Client_ID,
    'Authorization' :  "Bearer " + access_token
    }
    x = requests.get(URL, headers = head).json()['data']
    return x

def GetChannelIcalendar(Client_ID, access_token, broadcaster_id):
    URL = "https://api.twitch.tv/helix/schedule/icalendar?broadcaster_id="+broadcaster_id
    head = {
    'Client-ID' : Client_ID,
    'Authorization' :  "Bearer " + access_token
    }
    x = requests.get(URL, headers = head)
    return x #return un fichier .pyc ??

def GetBroadcasterSubscriptions(Client_ID, access_token, broadcaster_id):
    URL = "https://api.twitch.tv/helix/subscriptions?broadcaster_id="+broadcaster_id
    head = {
    'Client-ID' : Client_ID,
    'Authorization' :  "Bearer " + access_token
    }
    x = requests.get(URL, headers = head)
    return x

def GetChannelStreamSchedule(Client_ID, access_token, broadcaster_id):
    URL = "https://api.twitch.tv/helix/schedule?broadcaster_id="+broadcaster_id
    head = {
    'Client-ID' : Client_ID,
    'Authorization' :  "Bearer " + access_token
    }
    x = requests.get(URL, headers = head).json()
    return x
    #Ne trouve pas d'edt dans les 5 cas

def GetVideos(Client_ID, access_token, broadcaster_id):
    URL = "https://api.twitch.tv/helix/videos?broadcaster_id="+broadcaster_id
    head = {
    'Client-ID' : Client_ID,
    'Authorization' :  "Bearer " + access_token
    }
    x = requests.get(URL, headers = head).json()
    return x

def GetXX(Client_ID, access_token, broadcaster_id):
    URL = "https://api.twitch.tv/helix/streams?broadcaster_id="+broadcaster_id
    head = {
    'Client-ID' : Client_ID,
    'Authorization' :  "Bearer " + access_token
    }
    x = requests.get(URL, headers = head).json()
    return x

def GetXXX(Client_ID, access_token, broadcaster_id):
    URL = "https://api.twitch.tv/helix/users?login="+broadcaster_id
    head = {
    'Client-ID' : Client_ID,
    'Authorization' :  "Bearer " + access_token
    }
    x = requests.get(URL, headers = head).json()['data'][0]
    return x

#################################################################################################

def CreateDataSet(Client_ID, access_token, streamer_names, X):     
    datas = []
    for i in range (len(streamer_names)):
        JSONContent = X(Client_ID, access_token, streamer_names[i])
        datas.append([JSONContent['id'], JSONContent['display_name'], JSONContent['view_count']])
    dataset = pd.DataFrame(datas)
    dataset.columns = ['Id', 'Name', 'Views']
    dataset.dropna(axis = 0, how = 'any', inplace = True)
    dataset.index = pd.RangeIndex(len(dataset.index))
    return dataset