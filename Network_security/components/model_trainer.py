from Network_security.exceptions.exception import NetworkSecurityException
from Network_security.logging.logger import logging
from Network_security.entity.config_entity import ModelTrainerConfig    
from Network_security.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from Network_security.constants.training_pipeline import MODEL_TRAINER_EXPECTED_SCORE
from Network_security.utils.utils import save_numpy_array,save_object,read_data,load_numpy_array,evaluate_model,load_object
from Network_security.utils.ml_utils.metric.classification_metric import get_classification_score
from Network_security.utils.ml_utils.model.estimator import NetworkModel
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import mlflow

import sys


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def track_mlflow(self,best_model,classifactionMetrics,split):
        try:
            mlflow.set_tracking_uri("http://localhost:5000")
            with mlflow.start_run():
                mlflow.log_metric("f1_score", classifactionMetrics.f1_score)
                mlflow.log_metric("precision_score", classifactionMetrics.precision_score)
                mlflow.log_metric("recall_score", classifactionMetrics.recall_score)
                if split == "test":
                    mlflow.sklearn.log_model(best_model, "model")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def train_model(self,x_train,y_train,x_test,y_test):
        logging.info("training the model")
        try:
            models={
                "Random Forest":RandomForestClassifier(),
                "Gradient Boosting":GradientBoostingClassifier(),
                "AdaBoost":AdaBoostClassifier(),
                "Logistic Regression":LogisticRegression(),
                "Decision Tree":DecisionTreeClassifier()
            
            }
            params={
                "Random Forest":{
                    'n_estimators':[100,200],
                    # 'max_depth':[None,10,20],
                    # 'min_samples_split':[2,5],
                    # 'min_samples_leaf':[1,2]
                },
                "Gradient Boosting":{
                    'n_estimators':[100,200],
                    # 'learning_rate':[0.01,0.1],
                    # 'max_depth':[3,5]
                },
                "AdaBoost":{
                    'n_estimators':[50,100],
                    # 'learning_rate':[0.01,0.1]
                },
                "Logistic Regression":{
                     'C':[0.01,0.1,1],
                      'max_iter':[100,200]
                },
                "Decision Tree":{
                    'max_depth':[None,10,20],
                    # 'min_samples_split':[2,5],
                    # 'min_samples_leaf':[1,2]
                }
            }
            report:dict=evaluate_model(x_train,y_train,x_test,y_test,models,params)
            #best model score
            logging.info(f"model report: {report}")
            best_model_name = max(report, key=lambda x: report[x]["test_score"])
            best_model_score = report[best_model_name]["test_score"]
            best_model = models[best_model_name]
            if best_model_score<MODEL_TRAINER_EXPECTED_SCORE:
                raise Exception(f"no best model found with score greater than {MODEL_TRAINER_EXPECTED_SCORE}")
            logging.info(f"best model found {best_model_name} with score {best_model_score}")
            best_model=models[best_model_name]
            best_model.fit(x_train,y_train)
            y_train_pred=best_model.predict(x_train)
            y_test_pred=best_model.predict(x_test)
            classification_train_score = get_classification_score(y_true=y_train, y_pred=y_train_pred)
            print("FIELDS:", vars(classification_train_score))
            self.track_mlflow(best_model=best_model, classifactionMetrics=classification_train_score, split="train") 

            classification_test_score = get_classification_score(y_true=y_test, y_pred=y_test_pred)
            self.track_mlflow(best_model=best_model, classifactionMetrics=classification_test_score, split="test")  

            preprocessor = load_object(filepath=self.data_transformation_artifact.transformed_object_file_path)
            network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
            save_object(filepath=self.model_trainer_config.trained_model_file_path, obj=network_model)
            logging.info(f"best model saved at {self.model_trainer_config.trained_model_file_path}")
            modelTrainerArtifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,trained_metrics=classification_train_score,test_metrics=classification_test_score)
            logging.info(f"model trainer artifact: {modelTrainerArtifact}")
            return modelTrainerArtifact
           

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            logging.info("initiating model trainer")
            train_arr=load_numpy_array(self.data_transformation_artifact.transformed_train_file_path)
            test_arr=load_numpy_array(self.data_transformation_artifact.transformed_test_file_path)
            x_train,y_train=train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test=test_arr[:,:-1],test_arr[:,-1]
            train=self.train_model(x_train,y_train,x_test,y_test)
            return train

        except Exception as e:
            raise NetworkSecurityException(e,sys)     