import fonctions

Client_ID = "uffof989s0jlx0rsqltxfd9twmhwbs"
streamer_name = ["korone","okayu","pekora","hachaama","kanata"]
access_token = fonctions.GetToken(Client_ID)

#for i in range (len(streamer_name)):    
    #Streamer_ID = fonctions.GetID(Client_ID, access_token, streamer_name[i])

#fonctions.GetTopGames(Client_ID, access_token)

#broadcaster_id=fonctions.GetID(Client_ID, access_token, streamer_name[1])
#fonctions.GetChannelIcalendar(Client_ID, access_token, broadcaster_id)

# user_id=fonctions.GetID(Client_ID, access_token, streamer_name[1])
# fonctions.GetFollowedStreams(Client_ID, access_token, user_id)

# broadcaster_id=fonctions.GetID(Client_ID, access_token, streamer_name[1])
# fonctions.GetBroadcasterSubscriptions(Client_ID, access_token, broadcaster_id)

user_id=fonctions.GetID(Client_ID, access_token, streamer_name[1])
fonctions.GetVideos(Client_ID, access_token, user_id)
