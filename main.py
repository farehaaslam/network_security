from Network_security.components.data_ingestion import DataIngestion
from Network_security.components.data_validation import DataValidation
from Network_security.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig,DataValidationConfig
if __name__=="__main__":
    data_ingestion_config=DataIngestionConfig(TrainingPipelineConfig())
    data_ingestion=DataIngestion(data_ingestion_config)
    data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
    print(data_ingestion_artifact)
    data_validation_config=DataValidationConfig(TrainingPipelineConfig())
    data_validation=DataValidation(data_ingestion_artifact,data_validation_config)
    data_validation_artifact=data_validation.initiate_data_validation()
    print(data_validation_artifact)
