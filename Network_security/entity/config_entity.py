from Network_security.constants import training_pipeline
from datetime import datetime
import os
class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifacts_name=training_pipeline.ARTIFACTS_DIR
        self.artifact_dir=os.path.join(self.artifacts_name,timestamp)
        self.timestamp: str = timestamp


class DataIngestionConfig:
    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir_name:str=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME) #artifacts/2023-09-28-12-00-00/data_ingestion
        self.feature_store_dir:str=os.path.join(self.data_ingestion_dir_name,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR) #artifacts/2023-09-28-12-00-00/data_ingestion/feature_store
        self.ingested_dir:str=os.path.join(self.data_ingestion_dir_name,training_pipeline.DATA_INGESTION_INGESTED_DIR_NAME) #artifacts/2023-09-28-12-00-00/data_ingestion/ingested
        self.train_test_split_ratio:float=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.database_name:str=training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name:str=training_pipeline.DATA_INGESTION_COLLECTION_NAME


