
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import numpy as np
import pandas as pd
from Network_security.logging.logger import logging
from Network_security.exceptions.exception import NetworkSecurityException
import pymongo
import sys
import json
load_dotenv()
uri=os.getenv("MONGO_DB_URI")

# # Create a new client and connect to the server

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

class ETLpipeline:
    def __init__(self):
        try:
            self.client = MongoClient(uri, server_api=ServerApi('1'))
            self.db = self.client["Network_security"]
        except Exception as e:
            logging.info("an error ocuured while connecting to mongodb")
            raise NetworkSecurityException(e, sys)

    def xlsx_to_json(self, file_path: str):
        try:
            df = pd.read_excel(file_path)
            df.reset_index(drop=True, inplace=True)

            records = df.to_dict(orient="records")

            return records

        except Exception as e:
            logging.info("an error ocuured while initializing the ETL pipeline")
            raise NetworkSecurityException(e, sys)
        
    def push_data_to_mongodb(self, collection_name: str, data: list):
        try:
            collection = self.db[collection_name]
            collection.insert_many(data)
            self.data=data
            logging.info(f"Data inserted successfully into the {collection_name} collection.")
            return len(self.data)
        except Exception as e:
            logging.info("an error ocuured while pushing data to mongodb")
            raise NetworkSecurityException(e, sys)
        
if __name__ =="__main__":
    DATA_PATH = os.path.join("Network_data", "Dataset-Phising-Website.xlsx")
    collection="network_data"
    networkobj=ETLpipeline()
    records=networkobj.xlsx_to_json(DATA_PATH)
    networkobj.push_data_to_mongodb(collection_name=collection,data=records)