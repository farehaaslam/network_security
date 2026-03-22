from Network_security.logging.logger import logging
from Network_security.components.data_ingestion import DataIngestion
from Network_security.components.data_validation import DataValidation
from Network_security.components.data_transformation import DatatTransformation
from Network_security.components.model_trainer import ModelTrainer
from Network_security.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
if __name__=="__main__":
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config=DataIngestionConfig(training_pipeline_config)
    data_ingestion=DataIngestion(data_ingestion_config)
    data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
    print(data_ingestion_artifact)
    data_validation_config=DataValidationConfig(training_pipeline_config)
    data_validation=DataValidation(data_ingestion_artifact,data_validation_config)
    data_validation_artifact=data_validation.initiate_data_validation()
    print(data_validation_artifact)
    data_transformation_config=DataTransformationConfig(training_pipeline_config)
    data_transformation=DatatTransformation(data_validation_artifact,data_transformation_config)
    data_transformation_artifact=data_transformation.initiate_data_transformation()
    print(data_transformation_artifact)
    logging.info("training started")
    model_trainer_config=ModelTrainerConfig(training_pipeline_config)
    model_trainer=ModelTrainer(model_trainer_config,data_transformation_artifact)
    model_trainer_artifact=model_trainer.initiate_model_trainer()
    logging.info(f"model trainer artifact :{model_trainer_artifact}")


