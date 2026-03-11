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

SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")

"""
data ingestion related constants 
"""
DATA_INGESTION_DATABASE_NAME:str="Network_security"
DATA_INGESTION_COLLECTION_NAME:str="network_data"  
DATA_INGESTION_DIR_NAME:str="data_ingestion" 
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR_NAME:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2

"""
data validation related constant
"""

DATA_VALIDATION_DIR_NAME="data_validation"
DATA_VALIDATION_VALID_DIR="validated"
DATA_VALIDATION_INVALID_DIR="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME="report.yaml"


