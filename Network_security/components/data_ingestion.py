import os
import sys
import pymongo
from Network_security.logging.logger import logging
from Network_security.entity.config_entity import DataIngestionConfig
from Network_security.exceptions.exception import NetworkSecurityException
from Network_security.entity.artifact_entity import DataIngestionArtifact
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()
uri=os.getenv("MONGO_DB_URI")
#read  data from mongodb
#write data to feature store
#split data into train and test set
#write data to ingested dir
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"Data Ingestion log started.")
            self.data_ingestion_config=data_ingestion_config    
        except Exception as e:
            raise NetworkSecurityException(e,sys) 

    def read_data_from_database(self):
        try:
            DataBase_name=self.data_ingestion_config.database_name
            Collection_name=self.data_ingestion_config.collection_name
            self.client = pymongo.MongoClient(uri)
            db = self.client[DataBase_name]
            collection = db[Collection_name]
            data = list(collection.find())
            df = pd.DataFrame(data)

            df.drop("_id", axis=1, inplace=True)
            df.replace('na', np.nan, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)  
    def export_data_to_feature_store(self,df:pd.DataFrame):
        try:
            feature_store_dir=self.data_ingestion_config.feature_store_dir
            os.makedirs(feature_store_dir,exist_ok=True)
            df.to_csv(os.path.join(feature_store_dir,"data.csv"),index=False,header=True)
            logging.info(f"data stored at {feature_store_dir} ")
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def  split_data(self,df:pd.DataFrame):
        try:
            logging.info("doing train test split")
            train,test=train_test_split(df,test_size=self.data_ingestion_config.train_test_split_ratio)
            #saving it to ingested
            ingested_dir_path=self.data_ingestion_config.ingested_dir
            os.makedirs(ingested_dir_path,exist_ok=True)
            train.to_csv(os.path.join(ingested_dir_path,"train.csv"),index=False,header=True)
            test.to_csv(os.path.join(ingested_dir_path,"test.csv"),index=False,header=True)
            logging.info(f"train and test csv file created")



        except Exception as e:
            raise NetworkSecurityException(e,sys)    

    def initiate_data_ingestion(self):
        try:
            
            df=self.read_data_from_database()
            df=self.export_data_to_feature_store(df)
            self.split_data(df)
            data_ingestion_artifact=DataIngestionArtifact(
                trained_file_path=os.path.join(self.data_ingestion_config.ingested_dir, self.data_ingestion_config.train_file_name),
                test_file_path=os.path.join(self.data_ingestion_config.ingested_dir, self.data_ingestion_config.test_file_name)
            )

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)          

