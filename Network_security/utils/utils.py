import yaml
from Network_security.exceptions.exception import NetworkSecurityException
from Network_security.logging.logger import logging
import os,sys
import numpy 
import dill
import pickle
import pandas as pd
import numpy as np

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