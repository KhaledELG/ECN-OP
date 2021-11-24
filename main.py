import fonctions
import pandas as pd
import matplotlib.pyplot as plt
import json
import config

# Information of the identifier and the token
Client_ID = config.Client_ID
access_token = fonctions.GetToken(Client_ID)
# Streamers names information
streamer_name = ["joueur_du_grenier","slipixxx"]
# Initialization of variables
all_data, datas = [], []
# Initialization of the tool for writing 
writer = pd.ExcelWriter('dataset.xlsx', engine='xlsxwriter')
# Start of the data collection loop
for i in range (len(streamer_name)):
    # Reading the first page of the JSON 
    # Get the streamer's ID
    broadcaster_id = fonctions.GetID(Client_ID, access_token, streamer_name[i])
    # Getting the videos on the first page
    JSONContent = fonctions.GetFirstVideos(Client_ID, access_token, broadcaster_id)
    # Start of data storage in datas
    for j in range (len(JSONContent['data'])):    
        datas.append([JSONContent['data'][j]['created_at'], JSONContent['data'][j]['duration'], JSONContent['data'][j]['user_name'], JSONContent['data'][j]['title'], JSONContent['data'][j]['view_count']])
    after = JSONContent['pagination']['cursor']
    # Obtaining videos and storing data for future pages
    stop = 0
    while(stop <1):
        JSONContent = fonctions.GetNextVideos(Client_ID, access_token, broadcaster_id,after)
        for j in range (len(JSONContent['data'])):
            datas.append([JSONContent['data'][j]['created_at'], JSONContent['data'][j]['duration'], JSONContent['data'][j]['user_name'], JSONContent['data'][j]['title'], JSONContent['data'][j]['view_count']])
        if (len(JSONContent['pagination']) !=0):
            after = JSONContent['pagination']['cursor']
        else:
            stop = 1 
    # Data layout
    dataset = pd.DataFrame(datas)
    dataset.columns = ['Created at', 'Duration', 'Nom du streamer', 'Title', 'Views']
    dataset.dropna(axis = 0, how = 'any', inplace = True)
    dataset.index = pd.RangeIndex(len(dataset.index))
    # Creation of the Excel file
    dataset.to_excel(writer, sheet_name=streamer_name[i], index=False)
    datas=[]
writer.save()
 

##Création_histogramme_data
# hist=plt.bar(df['Name'],df['Views'])
# plt.show()
#plt.savefig("pandas_hist_01.png", bbox_inches='tight', dpi=100)