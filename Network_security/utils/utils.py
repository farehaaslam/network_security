from sklearn.metrics import accuracy_score
import yaml
from Network_security.exceptions.exception import NetworkSecurityException
from Network_security.logging.logger import logging
from sklearn.model_selection import GridSearchCV
import os,sys
import pickle
import pandas as pd
import numpy as np
import mlflow

def read_yaml_file(file_path)->dict:
    try:
        with open(file_path,"r") as file:
            return yaml.safe_load(file)  #return in the form of dictionary
    except Exception as e:
        NetworkSecurityException(e,sys)

def read_data(file_path)->pd.DataFrame:
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml(filepath:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(filepath):
                os.remove(filepath)
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath,"w") as file:
            yaml.dump(content,file)        
    except Exception as e:
        raise NetworkSecurityException(e,sys)    
    
def save_numpy_array(filepath:str,arr:np.array):
    try:
        logging.info("saving the numpy array ")
        dir_path=os.path.dirname(filepath)
        os.makedirs(dir_path,exist_ok=True)
        with open(filepath,"wb")as file:
            np.save(file,arr)
    except Exception as e:
        raise NetworkSecurityException(e,sys) 
    
def save_object(filepath:str,obj:object):
    try:
        logging.info("stated saving preprocessor file")
        dir_path=os.path.dirname(filepath)
        os.makedirs(dir_path,exist_ok=True)
        with open(filepath,"wb")as file:
            pickle.dump(obj,file)
        logging.info("preprocessor file saved succesfully")   
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_object(filepath:str)->object:
    try:
        if not os.path.exists(filepath):
            raise Exception(f"file not found at {filepath}")    
        with open(filepath,"rb") as file:
            return pickle.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_array(filepath:str)->np.array:
    try:
        if not os.path.exists(filepath):
            raise Exception(f"file not found at {filepath}")    
        with open(filepath,"rb") as file:
            return np.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)    
    
def evaluate_model(x_train,y_train,x_test,y_test,models,params:dict)->dict:
    try:
        report={}
        logging.info("model evaluation started")

        for model_name,model in models.items():
            logging.info(f"evaluating {model_name}")
            gs=GridSearchCV(model,params[model_name],cv=5,n_jobs=-1)
            gs.fit(x_train,y_train)
            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)
            y_train_pred=model.predict(x_train)
            y_test_pred=model.predict(x_test)
            train_model_score=accuracy_score(y_train,y_train_pred)
            test_model_score=accuracy_score(y_test,y_test_pred)
            report[model_name]={
                "train_score":train_model_score,
                "test_score":test_model_score
            }
        return report    


    except Exception as e:
        NetworkSecurityException(e,sys)    