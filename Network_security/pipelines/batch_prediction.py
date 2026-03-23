from Network_security.exceptions.exception import NetworkSecurityException
from Network_security.logging.logger import logging 
from Network_security.utils.utils import load_object
from Network_security.utils.ml_utils.model.estimator import NetworkModel

import sys,os 
import pandas as pd

class BatchPredictionPipeline:
    def __init__(self,input_file:str):
        self.input_file=input_file

    def run_batch_prediction(self):
        try:
            logging.info("Batch prediction pipeline started")
            df=pd.read_csv(self.input_file) 
            if 'Result' in df.columns:
                X = df.drop('Result', axis=1)  # Remove target column
            else:
                X = df  # No target column, use all   
            preprocessor=load_object("final_model/preprocessing.pkl")
            model=load_object("final_model/model.pkl")

            predictions=NetworkModel(preprocessor=preprocessor, model=model)
            y_pred=predictions.predict(X)
            print(y_pred)
            df["predicted"]=y_pred
            os.makedirs("predicted_output", exist_ok=True)
            df.to_csv("predicted_output/output.csv",index=False)
            logging.info("Batch prediction pipeline completed successfully")
            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)