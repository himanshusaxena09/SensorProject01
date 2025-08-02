from pymongo import MongoClient
import pandas as pd
import json
import certifi

# MongoDB connection URI with TLS enforced
uri = "mongodb+srv://himanshu:James%409001@cluster0.noxunci.mongodb.net/?retryWrites=true&w=majority&tls=true"

# Use certifi to securely connect with MongoDB Atlas
client = MongoClient(uri, tlsCAFile=certifi.where())

# Create database and collection names
DATABASE_NAME = "james"
COLLECTION_NAME = "waferfault"

# Read CSV file (ensure the path is raw)
df = pd.read_csv(r"D:\DS_Himanshu_Files\DATA SCIENCE\Jupyter_Notebook\SENSOR PROJECT\notebooks\wafer_23012020_041211.csv")

# Drop the auto-generated index column
if "Unnamed: 0" in df.columns:
    df = df.drop("Unnamed: 0", axis=1)

# Convert to JSON format for MongoDB
json_record = list(json.loads(df.T.to_json()).values())

# Insert into MongoDB collection
client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)

print("✅ Data inserted into MongoDB successfully.")
