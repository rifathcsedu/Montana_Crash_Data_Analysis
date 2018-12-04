import numpy as np
import matplotlib.pyplot as plt
import random
import csv
from kmodes.kmodes import KModes

county=['Park_Point_2']
#county=['Gallatin_Point_1','Gallatin_Point_2','Madison_Point_1','Madison_Point_2','Park_Point_1','Park_Point_2']
for County in county:
    print("****************County: "+County+" *******************")
    Month,JUNCTION_RELATED,roadway,weather, road_cond,LIGHT_COND,CRASH_SEVERITY,COLLISION_TYPE = [], [],[],[],[],[],[],[]
    with open('/Users/usmp/Google Drive/Saidur_Matt_Term_Project/Points_to_Cluster/'+County+'.csv') as f:
        reader = csv.reader(f)
        next(reader) # Ignore the header row.
        for row in reader:
            # filter lat,road_cond to (approximate) map view:
            Month.append(row[0])
            JUNCTION_RELATED.append(row[1])
            roadway.append(row[2])
            weather.append( row[3] )
            road_cond.append( row[4] )
            LIGHT_COND.append(row[5])
            CRASH_SEVERITY.append(row[6])
            COLLISION_TYPE.append(row[7])
            
    data=[]
    columnNum=3
    numberofdata=len(Month)
    #threshhold=0.5*(1/(columnNum*numberofdata*0.01))
    threshhold=0.08
    # random categorical data
    for i in range(len(weather)):
        data.append([weather[i],road_cond[i],LIGHT_COND[i],roadway[i]])
        #data.append([weather[i],road_cond[i],LIGHT_COND[i]])
    
    #print(data)
    cluster=2
    flag=0
    while(cluster<4):
        km = KModes(n_clusters=cluster, init='Huang', n_init=5, verbose=1)
        clusters = km.fit_predict(data)
        print(km.cluster_centroids_)
        ModeData=km.cluster_centroids_
        i=len(ModeData)-1
        while(i>=0):
            temp=ModeData[i]
            j=0
            cnt=0
            while(j<numberofdata):
                #if(roadway[j]==temp[3] and weather[j]==temp[0] and road_cond[j]==temp[1] and LIGHT_COND[j]==temp[2]):
                #    cnt+=1
                if(weather[j]==temp[0] and road_cond[j]==temp[1] and LIGHT_COND[j]==temp[2]):
                    cnt+=1
                j+=1
            if((cnt/numberofdata)<threshhold):
                flag=1
                print("Cluster "+str(cluster)+", minimum percentage is "+str(cnt*100.0/numberofdata))
                break
            i-=1
        if(flag==1):
            break
        cluster+=1
            
    if(flag==1 and cluster>2):
        cluster-=1        
    cluster1=2
    print("Done\n\n*************Final Cluster is %d and Running KModes with final cluster********************"%cluster1)
    km = KModes(n_clusters=cluster1, init='Huang', n_init=5, verbose=1)
    clusters = km.fit_predict(data)
    print(km.cluster_centroids_)
    ModeData=km.cluster_centroids_
    i=len(ModeData)-1
    while(i>=0):
        temp=ModeData[i]
        j=0
        cnt=0
        while(j<numberofdata):
            if(roadway[j]==temp[3] and weather[j]==temp[0] and road_cond[j]==temp[1] and LIGHT_COND[j]==temp[2]):
                cnt+=1
            #if(weather[j]==temp[0] and road_cond[j]==temp[1] and LIGHT_COND[j]==temp[2]):
                #cnt+=1
            j+=1
        print("Final Cluster is "+str(cluster1)+", percentage of Kmode data "+str(temp)+" is "+str(cnt*100.0/numberofdata))
        i-=1
    print(threshhold)
    print(numberofdata)