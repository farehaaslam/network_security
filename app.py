import os,sys
import pymongo
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
from fastapi import FastAPI, File, Request, Response,UploadFile
app = FastAPI()
from uvicorn import run as app_run
mongodb_uri=os.getenv("MONGO_DB_URI")
print(mongodb_uri)
from Network_security.exceptions.exception import NetworkSecurityException
from Network_security.logging.logger import logging
from Network_security.pipelines.training_pipeline import TrainPipeline
from fastapi.middleware.cors import CORSMiddleware
from Network_security.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME,DATA_INGESTION_COLLECTION_NAME
from Network_security.pipelines.batch_prediction import BatchPredictionPipeline
client=pymongo.MongoClient(mongodb_uri)
database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]

origins=["*"]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_methods=["*"],allow_headers=["*"],allow_credentials=True)
@app.get("/")
def index():
    return Response(content="Welcome to Network Security API !!",status_code=200)
@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainPipeline()
        train_pipeline.run_pipeline()
        return Response(content="Training successful !!",status_code=200)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

@app.post("/predict")
async def predict_route(file: UploadFile=File(...)):
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # 2. Pass FILE PATH (string) to pipeline
        batch_prediction_pipeline=BatchPredictionPipeline(input_file=tmp_file_path)
        result=batch_prediction_pipeline.run_batch_prediction()
        print(result)
        
        # 3. Cleanup
        os.unlink(tmp_file_path)
        return Response(content="Prediction successful !!",status_code=200)

    except Exception as e:
        raise NetworkSecurityException(e,sys)

if __name__=="__main__":
    app_run(app,host="localhost", port=8000)
