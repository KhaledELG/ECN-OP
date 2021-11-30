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
datas = []
# Initialization of the tool for writing 
# writer = pd.ExcelWriter('dataset.xlsx', engine='xlsxwriter')
# Start of the data collection loop
for i in range (len(streamer_name)):
    # Creation of dataset
    datas = fonctions.CreateDataSet(streamer_name,datas,Client_ID, access_token, i)
    # Data layout
    dataset = pd.DataFrame(datas)
    dataset.columns = ['Created at', 'Duration', 'Streamer Name', 'Title', 'Views']
    dataset.dropna(axis = 0, how = 'any', inplace = True)
    dataset.index = pd.RangeIndex(len(dataset.index))
#     # Creation of the Excel file
#     dataset.to_excel(writer, sheet_name=streamer_name[i], index=False)
#     datas=[]
# writer.save()
 
# Start of data processing
# Calculation of views per streamer
ViewsPerStreamer = dataset.groupby(['Streamer Name'])['Views'].sum()
# Average video length per streamer
data_tmp=dataset
data_tmp['Duration'] = pd.to_datetime(data_tmp['Duration'])
AverageVideoLengthPerStreamer = ((data_tmp.groupby(['Streamer Name'])['Duration']).mean()).dt.time

# print(AverageVideoLengthPerStreamer)

# Création_histogramme_data
# hist=plt.bar(dataset['Streamer Name'],dataset['Views'])
# plt.show()
# plt.savefig("pandas_hist_01.png", bbox_inches='tight', dpi=100)