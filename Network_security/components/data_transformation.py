import os

from Network_security.exceptions.exception import NetworkSecurityException
from Network_security.logging.logger import logging
from Network_security.entity.config_entity import DataTransformationConfig
from Network_security.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from Network_security.constants.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS
from Network_security.utils.utils import save_numpy_array,save_object,read_data

import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
#steps
#initiate data transformation
# read train and test file
#dropping target column
#transfomation pipeline


class DatatTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformer_pipeline(self)->Pipeline:
        logging.info("initiating data tranformer pipeline with ")
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor:Pipeline=Pipeline([("imputer",imputer)])
            return processor
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("initiated data transformation")
        try:
            train_data=read_data(self.data_validation_artifact.valid_train_file_path)
            test_data=read_data(self.data_validation_artifact.valid_test_file_path)

            input_feature_train_data=train_data.drop(columns=[TARGET_COLUMN])
            target_feature_train_data=train_data[TARGET_COLUMN]
            target_feature_train_data=target_feature_train_data.replace(-1,0) # classes will be either 0 or 1

            input_feature_test_data=test_data.drop(columns=[TARGET_COLUMN])
            target_feature_test_data=test_data[TARGET_COLUMN]
            target_feature_test_data=target_feature_test_data.replace(-1,0) # classes will be either 0 or 1

            prepocessor=self.initiate_data_transformer_pipeline()
            transformed_input_train_feature=prepocessor.fit_transform(input_feature_train_data)
            transformed_input_test_feature=prepocessor.transform(input_feature_test_data)

            train_arr=np.c_[transformed_input_train_feature,target_feature_train_data]
            test_arr=np.c_[transformed_input_test_feature,target_feature_test_data]
            logging.info(f"saved the transformed train and test data in numpy array format")


            save_numpy_array(filepath=self.data_transformation_config.transformed_train_file_path,arr=train_arr)
            save_numpy_array(filepath=self.data_transformation_config.transformed_test_file_path,arr=test_arr)
            save_object(filepath=self.data_transformation_config.transformed_object_path,obj=prepocessor)
            logging.info(f"saved the preprocessor object")
            os.makedirs("final_model", exist_ok=True)
            save_object(
            filepath=os.path.join("final_model", "preprocessing.pkl"),
            obj=prepocessor
            )
            data_transformation_artifact=DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_path
                
            )
            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact



        except Exception as e:
            raise NetworkSecurityException(e,sys)