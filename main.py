from Network_security.components.data_ingestion import DataIngestion
from Network_security.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
if __name__=="__main__":
    data_ingestion_config=DataIngestionConfig(TrainingPipelineConfig())
    data_ingestion=DataIngestion(data_ingestion_config)
    data_ingestion.initiate_data_ingestion()