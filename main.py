import fonctions
import pandas as pd
import matplotlib.pyplot as plt


Client_ID = "uffof989s0jlx0rsqltxfd9twmhwbs"
streamer_name = ["ironmouse","nekomatokayu","usadapekora_hololive","akaihaato_hololive", "slipixxx"]
access_token = fonctions.GetToken(Client_ID)

df = fonctions.CreateDataSet(Client_ID, access_token, streamer_name, fonctions.GetXXX)
print(df['Name'])

##Création_Excel_data
# writer = pd.ExcelWriter('dataset.xlsx', engine='xlsxwriter')
# df.to_excel(writer, sheet_name='Sheet1', index=False)
# writer.save()

##Création_histogramme_data
# hist=plt.bar(df['Name'],df['Views'])
# plt.show()
#plt.savefig("pandas_hist_01.png", bbox_inches='tight', dpi=100)