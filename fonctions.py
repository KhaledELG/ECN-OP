#################################################################################################

import requests
import json
import pandas as pd
import config
import datetime

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
    print(AutCall.text)
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

def MostStreamedDay(test, streamer_name):
    tbl,i,lundi,mardi,mercredi,jeudi,vendredi,samedi,dimanche=[],0,0,0,0,0,0,0,0
    for j in range (len(streamer_name)) :
        ok=test['Created at'][i][:10].split('-') #extrait la date ligne i
        now = datetime.datetime(int(ok[0]), int(ok[1]), int(ok[2])).weekday() #donne le jour
        while test['Streamer Name'][i]==streamer_name[j]:
            if i+1<len(test): 
                i=i+1   
                if now == 0 : lundi=lundi+1
                elif now == 1 : mardi=mardi+1
                elif now == 2 : mercredi=mercredi+1
                elif now == 3 : jeudi=jeudi+1
                elif now == 4 : vendredi=vendredi+1
                elif now == 5 : samedi=samedi+1
                else : dimanche=dimanche+1
                ok=test['Created at'][i][:10].split('-') #extrait la date ligne i
                now = datetime.datetime(int(ok[0]), int(ok[1]), int(ok[2])).weekday() #donne le jour
            else : 
                ok=test['Created at'][i][:10].split('-') #extrait la date ligne i
                now = datetime.datetime(int(ok[0]), int(ok[1]), int(ok[2])).weekday() #donne le jour
                if now == 0 : lundi=lundi+1
                elif now == 1 : mardi=mardi+1
                elif now == 2 : mercredi=mercredi+1
                elif now == 3 : jeudi=jeudi+1
                elif now == 4 : vendredi=vendredi+1
                elif now == 5 : samedi=samedi+1
                else : dimanche=dimanche+1
                break
        tbl.append([lundi, mardi, mercredi, jeudi, vendredi, samedi , dimanche, test['Streamer Name'][i-1]])
        lundi,mardi,mercredi,jeudi,vendredi,samedi,dimanche=0,0,0,0,0,0,0
    return tbl

#################################################################################################

def CreateDataSet(streamer_name,datas,Client_ID, access_token, i):     
    # Reading the first page of the JSON 
    # Get the streamer's ID
    broadcaster_id = GetID(Client_ID, access_token, streamer_name[i])
    # Getting the videos on the first page
    JSONContent = GetFirstVideos(Client_ID, access_token, broadcaster_id)
    # Start of data storage in datas
    for j in range (len(JSONContent['data'])):    
        datas.append([JSONContent['data'][j]['created_at'], DurationFormat(JSONContent['data'][j]['duration']), JSONContent['data'][j]['user_name'], JSONContent['data'][j]['title'], JSONContent['data'][j]['view_count']])
    after = JSONContent['pagination']['cursor']
    # Obtaining videos and storing data for future pages
    stop = 0
    while(stop <1):
        JSONContent = GetNextVideos(Client_ID, access_token, broadcaster_id,after)
        for j in range (len(JSONContent['data'])):
            datas.append([JSONContent['data'][j]['created_at'], DurationFormat(JSONContent['data'][j]['duration']), JSONContent['data'][j]['user_name'], JSONContent['data'][j]['title'], JSONContent['data'][j]['view_count']])
        if (len(JSONContent['pagination']) !=0):
            after = JSONContent['pagination']['cursor']
        else:
            stop = 1 
    return datas
    
#################################################################################################

def DurationFormat(str):
    my_str=[]
    if str.find('h')!=-1:
        time="hms"
    elif str.find('m')!=-1:
        time="ms"
    else:
        time="s"
    for i in range (len(time)):
        my_str.append(str.split(time[i])[0])
        str=str.split(time[i])[1]

    if len(my_str) == 1 :
        if len(my_str[0])>1:
            str='00:00:'+ my_str[0]
        else: str='00:00:0'+my_str[0]
    elif len(my_str) == 2 :
        if len(my_str[0])>1 and len(my_str[1])>1:
            str= '00:' + my_str[0] + ':' + my_str[1]
        elif len(my_str[0])>1 and len(my_str[1])<=1:
            str= '00:' + my_str[0] + ':0' + my_str[1]
        elif len(my_str[0])<=1 and len(my_str[1])>1:
            str= '00:0' + my_str[0] + ':' + my_str[1]
        else : str= '00:0' + my_str[0] + ':0' + my_str[1]
    elif len(my_str) == 3 :
        if len(my_str[0])>1 and len(my_str[1])>1 and len(my_str[2])>1:
            str= my_str[0] + ':' + my_str[1] + ':' + my_str[2]
        elif len(my_str[0])>1 and len(my_str[1])>1 and len(my_str[2])<=1:
            str= my_str[0] + ':' + my_str[1] + ':0' + my_str[2]
        elif len(my_str[0])>1 and len(my_str[1])<=1 and len(my_str[2])>1:
            str= my_str[0] + ':0' + my_str[1] + ':' + my_str[2]
        elif len(my_str[0])>1 and len(my_str[1])<=1 and len(my_str[2])<=1:
            str= my_str[0] + ':0' + my_str[1] + ':0' + my_str[2]
        elif len(my_str[0])<=1 and len(my_str[1])>1 and len(my_str[2])>1:
            str= '0' + my_str[0] + ':' + my_str[1] + ':' + my_str[2]
        elif len(my_str[0])<=1 and len(my_str[1])>1 and len(my_str[2])<=1:
            str= '0' + my_str[0] + ':' + my_str[1] + ':0' + my_str[2]
        elif len(my_str[0])<=1 and len(my_str[1])<=1 and len(my_str[2])>1:
            str= '0' + my_str[0] + ':0' + my_str[1] + ':' + my_str[2]
        else : str= '0' + my_str[0] + ':0' + my_str[1] + ':0' + my_str[2]
    return str


