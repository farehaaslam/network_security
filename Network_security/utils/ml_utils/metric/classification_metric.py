from Network_security.exceptions.exception import NetworkSecurityException
from Network_security.logging.logger import logging
from sklearn.metrics import f1_score,accuracy_score,precision_score,recall_score
from Network_security.entity.artifact_entity import ModelEvaluationArtifact
import sys
def get_classification_score(y_true,y_pred)->ModelEvaluationArtifact:
    try:
        f1_score_value=f1_score(y_true,y_pred)
        accuracy_score_value=accuracy_score(y_true,y_pred)
        precision_score_value=precision_score(y_true,y_pred)
        recall_score_value=recall_score(y_true,y_pred)
        model_evaluation_artifact=ModelEvaluationArtifact(
            f1_score=f1_score_value,
            precision_score=precision_score_value,
            recall_score=recall_score_value
        )
        return model_evaluation_artifact
    except Exception as e:
        raise NetworkSecurityException(e,sys)