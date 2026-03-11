import pandas as pd

from Network_security.exceptions.exception import NetworkSecurityException
from Network_security.logging.logger import logging
from Network_security.entity.config_entity import DataValidationConfig
from Network_security.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from scipy.stats import ks_2samp
import os,sys
from Network_security.constants.training_pipeline import SCHEMA_FILE_PATH
from Network_security.utils.utils import read_yaml_file,read_data,write_yaml


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
           raise NetworkSecurityException(e,sys)

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self.schema_config["columns"])
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {dataframe.shape[1]}")
            if dataframe.shape[1]==number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)    

    def validate_numerical_column_existence(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns=self.schema_config["numeric_columns"]
            logging.info(f"Required numerical columns: {numerical_columns}")
            dataframe_columns=dataframe.columns
            logging.info(f"Dataframe columns: {dataframe_columns}")
            for num_col in numerical_columns:
                if num_col not in dataframe_columns:
                    logging.info(f"Numerical column: {num_col} is not present in dataframe")
                    return False
            return True
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
        
    def detect_data_drift(self, base_data: pd.DataFrame, new_data: pd.DataFrame, threshold: float) -> bool:
        try:
            drift_report = {}
            status = False

            for column in base_data.columns:
                d1 = base_data[column]
                d2 = new_data[column]

                _, p_value = ks_2samp(d1, d2)

                drift_detected = p_value < threshold

                if drift_detected:
                    status = True

                drift_report[column] = {
                    "p_value": float(p_value),
                    "drift_detected": drift_detected
                }

            drift_report_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_path)

            os.makedirs(dir_path, exist_ok=True)

            write_yaml(drift_report_path, drift_report)

            return status

        except Exception as e:
            raise NetworkSecurityException(e, sys)
                
       

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            #read
            train_data=read_data(train_file_path)
            test_data=read_data(test_file_path)
            #validate number of column
            status=self.validate_number_of_columns(train_data)
            if not status:
                raise Exception(f"Train data does not have required number of columns")
            self.validate_number_of_columns(test_data)
            if not status:
                raise Exception(f"Test data does not have required number of columns")

            # is numerical column exist 
            status=self.validate_numerical_column_existence(train_data)
            if not status:
                raise Exception(f"Train data does not have all required numerical columns")
            status=self.validate_numerical_column_existence(test_data)
            if not status:
                raise Exception(f"Test data does not have all required numerical columns")
                #validate distribution 
            status=self.detect_data_drift(base_data=train_data,new_data=test_data,threshold=0.05)
            os.makedirs(self.data_validation_config.valid_data_dir, exist_ok=True)
            train_data.to_csv(self.data_validation_config.valid_train_file_path,index=False)
            test_data.to_csv(self.data_validation_config.valid_test_file_path,index=False)
            data_validation_artifact=DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
                    invalid_train_file_path=None,
                    invalid_test_file_path=None
            )  
            return data_validation_artifact         
        

           
        except Exception as e:
            raise NetworkSecurityException(e,sys)
       
