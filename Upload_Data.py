from pymongo.mongo_client import MongoClient
import pandas as pd
import json

uri="mongodb+srv://himanshu:James%409001@cluster0.noxunci.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

#create a new client and connectt to server
client = MongoClient(uri)

#create database name and collection name
DATABASE_NAME="james"
COLLECTION_NAME='waferfault'

df=pd.read_csv("D:\DS_Himanshu_Files\DATA SCIENCE\Jupyter_Notebook\SENSOR PROJECT\notebooks\wafer_23012020_041211.csv")

df=df.drop("Unnamed: 0",axis=1)

json_record=list(json.loads(df.T.to_json()).values())

client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)