# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 22:04:07 2017

@author: Marihebert
"""

import math
import json
import sys

# looking for user's social network
def friendship(friend, dat):
    for i in range(len(friend)):
        for j in range(len(dat)):
            if dat[j]["event_type"]=="befriend":
                if dat[j]["id1"]==friend[i]:
                    if (dat[j]["id2"] in friend) == False:
                        friend.append(dat[j]["id2"])                    
                if dat[j]["id2"]==friend[i]:
                    if (dat[j]["id1"] in friend) == False:
                        friend.append(dat[j]["id1"])
            if dat[j]["event_type"]=="unfriend":
                if dat[j]["id1"] in friend and dat[j]["id1"]<>friend[0]:
                    friend.remove(dat[j]["id1"])
                if dat[j]["id2"] in friend and dat[j]["id2"]<>friend[0]:
                    friend.remove(dat[j]["id2"])
                
    return friend
# mean calculation
def calc_mean(Vals,T_used):
    sum=0
    for k in range(T_used):
        sum=sum+float(Vals[k]['amount'])
    mean=sum/T_used
    return mean    
#standard deviation calculation    
def calc_sd(Vals,T_used,mean):
    sum2=0
    for k in range(T_used):
        sum2=sum2+math.pow(float(Vals[k]['amount'])-mean,2)
    sd=math.sqrt(sum2/T_used)
    return sd
    
def main(file_batch,file_str,file_out):
    #loading historical data
    dat_his=[]
    for line in open(file_batch,'r'):
    #with open(file_batch,'r') as fp:
	#for line in fp:
       dat_his.append(json.loads(line))
    #fp.close()

    T=int(dat_his[0]["T"])
    D=int(dat_his[0]["D"])
        
    
    #loading actual data
    dat_str=[]
    for line in open(file_str,'r'):
    #with open(file_str,'r') as fp:
	#for line in fp:
       dat_str.append(json.loads(line))
    #fp.close()
    
    #Sorting data by timestamps
    dat_up=sorted(dat_his[1:len(dat_his)], key=lambda k: k['timestamp'], reverse=False)
    dat_down=sorted(dat_his[1:len(dat_his)], key=lambda k: k['timestamp'], reverse=True)
    
    #looking for purchase events
    out=[]
    dat_index=[]
    dat_meansd=[]
    idf=[]
    for i in range(len(dat_str)):
        sw=0
        if dat_str[i]["event_type"]=="purchase":
            #reading id purchases from historical data
            if [dat_str[i]["id"]] in dat_index:
                index=dat_index([dat_str[i]["id"]])
                mean=dat_meansd[index][0]
                sd=dat_meansd[index][1]
                sw=1
            else:
            
                idf=[dat_str[i]["id"]]
                D_used=max(1,D)
                for k in range(D_used):
                    idf=friendship(idf, dat_up)
        
                idf=idf[1:len(idf)]        
                pur=[]
                for j in range(len(dat_down)):            
                    if dat_down[j]["event_type"]=="purchase":
                        if dat_down[j]["id"] in idf:
                            pur.append(dat_down[j])
                
                if len(pur)>=2 and T>=2:                    
                    # calculating mean
                    T_used=min(len(pur),T)
                    mean = calc_mean(pur,T_used)
                    
                    #Calculating Standard Deviation        
                    sd=calc_sd(pur,T_used,mean)
                    sw=1
                    
            if sw==1:
                if float(dat_str[i]['amount'])>3*sd:
                    out.append({'event_type':dat_str[i]["event_type"], 'timestamp':dat_str[i]["timestamp"], 'id':dat_str[i]["id"],"amount":dat_str[i]["amount"],"mean":str(float("{0:.2f}".format(mean))), "sd":str(float("{0:.2f}".format(sd)))})
            	dat_index.append(dat_str[i]["id"])
            	dat_meansd.append([[mean],[sd]])
   # saving output data 
    with open(file_out,'w') as Json_out:
        for i in range(len(out)):
            Json_out.write(json.dumps(out[i])+'\n')
        Json_out.write('\n')

   #updating batch_log.json file 
    with open(file_batch,'w') as Json_update:
        Json_update.write(json.dumps(dat_his[0])+'\n')
        for i in range(len(dat_str)):
            Json_update.write(json.dumps(dat_str[i])+'\n')
        for i in range(1,len(dat_his)):
            Json_update.write(json.dumps(dat_his[i])+'\n')


if __name__=="__main__":
    file_batch=sys.argv[1]
    file_str=sys.argv[2]
    file_out=sys.argv[3]
    main(file_batch, file_str, file_out)
