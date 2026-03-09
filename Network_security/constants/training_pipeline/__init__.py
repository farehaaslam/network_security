import os
import sys

"""
training pipeline related COMMON constants 
"""
TARGET_COLUMN:str="Result"
PIPELINE_NAME:str="Network_security"
ARTIFACTS_DIR:str="artifacts"
FILE_NAME:str="phishing_data.csv"
TEST_FILE_NAME:str="test.csv"
TRAIN_FILE_NAME:str="train.csv"

"""
data ingestion related constants 
"""
DATA_INGESTION_DATABASE_NAME:str="Network_security"
DATA_INGESTION_COLLECTION_NAME:str="network_data"  
DATA_INGESTION_DIR_NAME:str="data_ingestion" 
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR_NAME:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2
