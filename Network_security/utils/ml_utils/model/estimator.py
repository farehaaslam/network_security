from Network_security.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
import os,sys
from Network_security.exceptions.exception import NetworkSecurityException
from Network_security.logging.logger import logging
class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def predict(self,X):
        try:
            logging.info("predicting the data using model")
            x_transformed=self.preprocessor.transform(X)
            return self.model.predict(x_transformed)
        except Exception as e:
            raise NetworkSecurityException(e,sys)