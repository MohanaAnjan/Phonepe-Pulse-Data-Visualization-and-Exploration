
import PIL
from PIL import Image
import os
import json
import pandas as pd
import numpy as np
import requests
import pymysql
import git

# [SQL libraries]
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
import pymysql
import plotly.express as px

import git
#url="https://github.com/PhonePe/pulse.git"
#dis="D:/GUVI/Capstone Project 2"
#from git import Repo
#Repo.clone_from(url,dis)





#**Connection to SQL**

connect=pymysql.connect(host="127.0.0.1",
                                user="root",
                                password=str(1234),
                                database="phonepe",
                                port=3306)
cursor=connect.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS phonepe')
cursor.close()
connect.close()

engine = create_engine("mysql+pymysql://root:1234@127.0.0.1:3306/phonepe")
connection = engine.connect()

conn = pymysql.connect(host="127.0.0.1", user='root', password="1234", database='phonepe')
cursor = conn.cursor()


#agg_trans
path1=("D:GUVI/Capstone Project 2/data/aggregated/transaction/country/india/state/")
Agg_state_list1=os.listdir(path1)

columns1={"States":[],"Years":[],"Quarter":[],"Transaction_name":[],"Transaction_count":[],"Transaction_amount":[]}
for i in Agg_state_list1:
    p_i=path1+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['transactionData']:

                name=z['name']
                count=z["paymentInstruments"][0]["count"]
                amount=z["paymentInstruments"][0]["amount"]
                columns1['Transaction_name'].append(name)
                columns1['Transaction_count'].append(count)
                columns1['Transaction_amount'].append(amount)
                columns1['States'].append(i)
                columns1['Years'].append(j)
                columns1['Quarter'].append(int(k.strip('.json')))

AGGREGATE_TRANSACTION_DATA=pd.DataFrame(columns1)


#aggregate_user

path2=("D:GUVI/Capstone Project 2/data/aggregated/user/country/india/state/")
Agg_state_list2=os.listdir(path2)
columns2={"States":[],"Years":[],"Quarter":[],"Brands":[],"Transaction_count":[],"Percentage":[]}
for i in Agg_state_list2:
    p_i=path2+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            B=json.load(Data)
            if B and B.get("data") and B["data"].get("usersByDevice"):
                for a in B["data"]["usersByDevice"]:         
                    brand=a["brand"]
                    count=a["count"]
                    percentage=a["percentage"]
                    columns2['Brands'].append(brand)
                    columns2['Transaction_count'].append(count)
                    columns2['Percentage'].append(percentage * 100)
                    columns2['States'].append(i)
                    columns2['Years'].append(j)
                    columns2['Quarter'].append(int(k.strip('.json')))

AGGREGATE_USER_DATA=pd.DataFrame(columns2)

#map transaction
path3=("D:GUVI/Capstone Project 2/data/map/transaction/hover/country/india/state/")
Agg_state_list3=os.listdir(path3)


columns3={"States":[],"Years":[],"Quarter":[],"District":[],"Transaction_count":[],"Transaction_amount":[]}
for i in Agg_state_list3:
    p_i=path3+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for y in D['data']['hoverDataList']:
                District=y['name']
                count=y["metric"][0]["count"]
                amount=y["metric"][0]["amount"]
                columns3['District'].append(District)
                columns3['Transaction_count'].append(count)
                columns3['Transaction_amount'].append(amount)
                columns3['States'].append(i)
                columns3['Years'].append(j)
                columns3['Quarter'].append(int(k.strip('.json')))


MAP_TRANSACTION_DATA=pd.DataFrame(columns3)

#mapuser
path4 = "D:/GUVI/Capstone Project 2/data/map/user/hover/country/india/state/"
Agg_state_list4 = os.listdir(path4)

columns4 = {"States": [], "Years": [], "Quarter": [], "Districts": [], "RegisteredUser": [], "AppOpens": []}

for i in Agg_state_list4:
    p_i = path4 + i + "/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + j + "/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + k
            with open(p_k, 'r') as Data:
                D = json.load(Data)

                for m in D['data']['hoverData'].items():
                    district = m[0]
                    registereduser = m[1]["registeredUsers"]
                    appopens = m[1]["appOpens"]
                    columns4["Districts"].append(district)
                    columns4["RegisteredUser"].append(registereduser)
                    columns4["AppOpens"].append(appopens)
                    columns4["States"].append(i)
                    columns4["Years"].append(j.strip(".json"))
                    columns4["Quarter"].append(int(k.strip(".json")))

MAP_USER_DATA = pd.DataFrame(columns4)

#top_transaction
path5=("D:GUVI/Capstone Project 2/data/top/transaction/country/india/state/")
Agg_state_list5=os.listdir(path5)

columns5 = {"States":[], "Years":[], "Quarter":[], "Pincodes":[], "Transaction_count":[], "Transaction_amount":[]}

for i in Agg_state_list5:
    p_i=path5+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for n in D["data"]["pincodes"]:
                entityName = n["entityName"]
                count = n["metric"]["count"]
                amount = n["metric"]["amount"]
                columns5["Pincodes"].append(entityName)
                columns5["Transaction_count"].append(count)
                columns5["Transaction_amount"].append(amount)
                columns5["States"].append(i)
                columns5["Years"].append(j)
                columns5["Quarter"].append(int(k.strip(".json")))

TOP_TRANSACTION_DATA=pd.DataFrame(columns5)


##topuser
path6=("D:GUVI/Capstone Project 2/data/top/user/country/india/state/")
Agg_state_list6=os.listdir(path6)

columns6 = {"States":[], "Years":[], "Quarter":[], "Pincodes":[], "RegisteredUsers":[]}
for i in Agg_state_list6:
    p_i=path6+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for h in D['data']['pincodes']:
                name = h["name"]
                registeredusers = h["registeredUsers"]
                columns6["Pincodes"].append(name)
                columns6["RegisteredUsers"].append(registeredusers)
                columns6["States"].append(i)
                columns6["Years"].append(j)
                columns6["Quarter"].append(int(k.strip(".json")))

TOP_USER_DATA=pd.DataFrame(columns6)


#**Connection to SQL**

connect=pymysql.connect(host="127.0.0.1",
                                user="root",
                                password="1234",
                                database="phonepe",
                                port=3306)
cursor=connect.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS phonepe')
cursor.close()
connect.close()

engine = create_engine("mysql+pymysql://root:1234@127.0.0.1:3306/phonepe")
connection = engine.connect()

conn = pymysql.connect(host="127.0.0.1", user='root', password="1234", database='phonepe')
cursor = conn.cursor()

#1
AGGREGATE_TRANSACTION_DATA.to_sql(name="aggregated_transaction", con=engine,schema="phonepe",if_exists = 'replace', index=False,
                                 dtype={'States': sqlalchemy.types.VARCHAR(length=100),
                                       'Years': sqlalchemy.types.Integer,
                                       'Quarter': sqlalchemy.types.Integer,
                                       'Transaction_name': sqlalchemy.types.VARCHAR(length=100),
                                       'Transaction_count': sqlalchemy.types.Integer,
                                       'Transaction_amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})

#2
AGGREGATE_USER_DATA.to_sql(name="aggregated_user", con=engine,schema="phonepe",if_exists = 'replace', index=False,
                     dtype={'States': sqlalchemy.types.VARCHAR(length=50),
                            'Years': sqlalchemy.types.Integer,
                            'Quarter': sqlalchemy.types.Integer,
                            'Brands': sqlalchemy.types.VARCHAR(length=50),
                            'Transaction_count': sqlalchemy.types.Integer,
                            'Percentage': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})

#3
MAP_TRANSACTION_DATA.to_sql(name="map_transaction", con=engine,schema="phonepe",if_exists = 'replace', index=False,
                          dtype={'States': sqlalchemy.types.VARCHAR(length=100),
                            'Years': sqlalchemy.types.Integer,
                            'Quarter': sqlalchemy.types.Integer,
                            'Transaction_name': sqlalchemy.types.VARCHAR(length=100),
                            'Transaction_count': sqlalchemy.types.Integer,
                            'Transaction_amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})


#4
MAP_USER_DATA.to_sql(name="map_user", con=engine,schema="phonepe",if_exists = 'replace', index=False,
                    dtype={'States': sqlalchemy.types.VARCHAR(length=100),
                            'Years': sqlalchemy.types.Integer,
                            'Quarter': sqlalchemy.types.Integer,
                            "Districts": sqlalchemy.types.VARCHAR(length=100),
                            "RegisteredUser":sqlalchemy.types.Integer,
                            "AppOpens":sqlalchemy.types.Integer})

#5
TOP_TRANSACTION_DATA.to_sql(name="top_transaction", con=engine,schema="phonepe",if_exists = 'replace', index=False,
                        dtype={'States': sqlalchemy.types.VARCHAR(length=100),
                            'Years': sqlalchemy.types.Integer,
                            'Quarter': sqlalchemy.types.Integer,
                            "Pincodes": sqlalchemy.types.Integer,
                            "Transaction_count":sqlalchemy.types.Integer,
                            "Transaction_amount":sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})     


#6
TOP_USER_DATA.to_sql(name="top_user", con=engine,schema="phonepe",if_exists = 'replace', index=False,
                        dtype={'States': sqlalchemy.types.VARCHAR(length=250),
                            'Years': sqlalchemy.types.Integer,
                            'Quarter': sqlalchemy.types.Integer,
                            "Pincodes": sqlalchemy.types.Integer,
                            "RegisteredUsers":sqlalchemy.types.Integer})

engine = create_engine("mysql+pymysql://root:1234@127.0.0.1:3306/phonepe")
connection = engine.connect()


