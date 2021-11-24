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

#TODO : See if it is possible to have new getters

# Defines the function determining the information of the first page of the JSON
def GetFirstVideos(Client_ID, access_token, broadcaster_id):
    URL = "https://api.twitch.tv/helix/videos?user_id="+broadcaster_id
    head = {
    'Client-ID' : Client_ID,
    'Authorization' :  "Bearer " + access_token
    }
    x = requests.get(URL, headers = head).json()
    return x

# Defines the function determining the information of the next pages of the JSON
def GetNextVideos(Client_ID, access_token, broadcaster_id, after):
    URL = "https://api.twitch.tv/helix/videos?user_id="+broadcaster_id+"&after="+after
    head = {
    'Client-ID' : Client_ID,
    'Authorization' :  "Bearer " + access_token
    }
    x = requests.get(URL, headers = head).json()
    return x

#################################################################################################

#TODO : Correct this part

def CreateDataSet(Client_ID, access_token, streamer_names, X,j):     
    datas = []
    for i in range (len(streamer_names)):
        JSONContent = X(Client_ID, access_token, GetID(Client_ID, access_token, streamer_names[i]))['data'][j]
        datas.append([JSONContent['created_at'], JSONContent['duration'], JSONContent['id'], JSONContent['title'], JSONContent['view_count']])
    dataset = pd.DataFrame(datas)
    dataset.columns = ['Created at', 'Duration', 'Video id', 'Title', 'Views']
    dataset.dropna(axis = 0, how = 'any', inplace = True)
    dataset.index = pd.RangeIndex(len(dataset.index))
    return dataset