import fonctions
import pandas as pd
import matplotlib.pyplot as plt
import json
import config
import datetime

# Information of the identifier and the token
Client_ID = config.Client_ID
access_token = fonctions.GetToken(Client_ID)
# Streamers names information
streamer_name = ["ironmouse", "nyanners", "silvervale", "apricot", "zentreya", "projektmelody", "hajime", "veibae"]
# Initialization of variables
datas = []
# Initialization of the tool for writing 
# writer = pd.ExcelWriter('dataset.xlsx', engine='xlsxwriter')
# Start of the data collection loop
for i in range (len(streamer_name)):
    # Creation of dataset
    datas = fonctions.CreateDataSet(streamer_name,datas,Client_ID, access_token, i)
print()