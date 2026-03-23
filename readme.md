# 🛡️ Network Security — Phishing Website Detection

An end-to-end **Machine Learning** system for detecting phishing websites. The project ingests website feature data, runs it through a full ML pipeline (ingestion → validation → transformation → training), and exposes a **FastAPI** REST API for real-time and batch predictions. Experiment tracking is handled by **MLflow** with remote logging via **DagShub**.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Dataset](#dataset)
- [ML Pipeline](#ml-pipeline)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Load Data into MongoDB](#load-data-into-mongodb)
- [Usage](#usage)
  - [Train the Model](#train-the-model)
  - [Run the FastAPI Server](#run-the-fastapi-server)
  - [Run with Docker](#run-with-docker)
- [API Reference](#api-reference)
- [Model Information](#model-information)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Phishing attacks trick users into visiting fraudulent websites that mimic legitimate ones to steal credentials, financial data, or personal information. This project builds a **binary classifier** that distinguishes phishing websites from legitimate ones using 30 URL and page-level features extracted from each website.

The system is designed as a production-ready ML service with:
- A modular, component-based training pipeline
- Schema validation and data drift detection
- Hyperparameter tuning via GridSearchCV
- Experiment tracking with MLflow and DagShub
- A FastAPI web service for training and batch prediction
- AWS S3 integration for artifact syncing

---

## Features

- ✅ **End-to-end ML pipeline**: data ingestion → validation → transformation → training
- ✅ **Multiple classifiers**: Random Forest, Gradient Boosting, AdaBoost, Logistic Regression, Decision Tree
- ✅ **Automated hyperparameter tuning** with GridSearchCV (5-fold cross-validation)
- ✅ **Schema validation** and data drift detection
- ✅ **MLflow + DagShub** experiment tracking
- ✅ **FastAPI** REST API with training and batch prediction endpoints
- ✅ **MongoDB** as the data store for raw feature records
- ✅ **AWS S3** syncing for model artifacts
- ✅ **Docker** support for containerised deployment

---

## Architecture

```
Excel Dataset (.xlsx)
        │
        ▼
   push_data.py  ──────────────────────► MongoDB
   (ETLpipeline)                        (network_data collection)
                                                │
                                                ▼
                                      DataIngestion
                                     (train.csv / test.csv)
                                                │
                                                ▼
                                      DataValidation
                               (schema check + drift detection)
                                                │
                                                ▼
                                    DataTransformation
                                      (KNN imputation)
                                                │
                                                ▼
                                       ModelTrainer
                                  (GridSearchCV + MLflow)
                                                │
                                                ▼
                              final_model/model.pkl
                              final_model/preprocessing.pkl
                                                │
                        ┌───────────────────────┤
                        │                       │
                        ▼                       ▼
              FastAPI /train            FastAPI /predict
                                   (BatchPredictionPipeline)
                                                │
                                                ▼
                                  predicted_output/output.csv
```

---

## Dataset

The dataset is sourced from the **UCI Machine Learning Repository** and contains **11,055 website samples**, each described by 30 features.

| Property | Detail |
|----------|--------|
| **File** | `Network_data/Dataset-Phising-Website.xlsx` |
| **Samples** | ~11,055 websites |
| **Features** | 30 numerical features (all int64) |
| **Target** | `Result` — `1` (Phishing) or `-1` (Legitimate) |

### Feature List

| Feature | Description |
|---------|-------------|
| `having_IP_Address` | URL uses IP address instead of domain name |
| `URL_Length` | Total length of the URL |
| `Shortining_Service` | URL uses a shortening service (bit.ly, etc.) |
| `having_At_Symbol` | `@` symbol present in URL |
| `double_slash_redirecting` | `//` redirect present after the protocol |
| `Prefix_Suffix` | Hyphen `-` in domain name |
| `having_Sub_Domain` | Number of sub-domains in the URL |
| `SSLfinal_State` | HTTPS certificate status |
| `Domain_registeration_length` | Domain registration duration |
| `Favicon` | Favicon loaded from external domain |
| `port` | Non-standard port used in URL |
| `HTTPS_token` | "HTTPS" token in the domain part |
| `Request_URL` | Percentage of external objects in the page |
| `URL_of_Anchor` | Percentage of `<a>` tags with external links |
| `Links_in_tags` | Percentage of links in `<meta>`, `<script>`, `<link>` tags |
| `SFH` | Server Form Handler |
| `Submitting_to_email` | `mailto:` used in form action |
| `Abnormal_URL` | Host name not in URL |
| `Redirect` | Number of redirects |
| `on_mouseover` | `onMouseOver` changes status bar |
| `RightClick` | Right-click disabled |
| `popUpWidnow` | Pop-up window with text fields |
| `Iframe` | Uses invisible `<iframe>` |
| `age_of_domain` | Age of the registered domain |
| `DNSRecord` | No DNS record found |
| `web_traffic` | Website traffic rank (Alexa) |
| `Page_Rank` | Google PageRank |
| `Google_Index` | Page is indexed by Google |
| `Links_pointing_to_page` | Number of links pointing to the page |
| `Statistical_report` | Host in top phishing IPs/domains list |

---

## ML Pipeline

The pipeline is broken into four sequential components:

| Step | Component | Description |
|------|-----------|-------------|
| 1 | **DataIngestion** | Fetches records from MongoDB and exports them as train/test CSVs (80/20 split) |
| 2 | **DataValidation** | Validates column count, data types, and detects data drift using KS test |
| 3 | **DataTransformation** | Applies KNN imputation (`n_neighbors=3`) to handle missing values; serialises the preprocessor |
| 4 | **ModelTrainer** | Trains five classifier families with GridSearchCV; selects the best model by test accuracy; logs all runs to MLflow |

### Models Evaluated

| Model | Hyperparameters Searched |
|-------|--------------------------|
| Random Forest | `n_estimators`: 100, 200 |
| Gradient Boosting | `n_estimators`: 100, 200 |
| AdaBoost | `n_estimators`: 50, 100 |
| Logistic Regression | `C`: 0.01, 0.1, 1 · `max_iter`: 100, 200 |
| Decision Tree | `max_depth`: None, 10, 20 |

The best model must achieve **at least 60% accuracy** to be promoted to `final_model/`.

### Evaluation Metrics

- **F1 Score**
- **Precision**
- **Recall**

---

## Project Structure

```
network_security/
├── Network_security/                  # Main Python package
│   ├── components/                    # Pipeline stage implementations
│   │   ├── data_ingestion.py          # MongoDB → train/test CSVs
│   │   ├── data_validation.py         # Schema validation & drift detection
│   │   ├── data_transformation.py     # KNN imputation preprocessing
│   │   └── model_trainer.py           # Model training + MLflow tracking
│   ├── pipelines/                     # Pipeline orchestrators
│   │   ├── training_pipeline.py       # Full train pipeline + S3 sync
│   │   └── batch_prediction.py        # Batch inference pipeline
│   ├── entity/                        # Config & artifact dataclasses
│   │   ├── config_entity.py
│   │   └── artifact_entity.py
│   ├── constants/
│   │   └── training_pipeline/
│   │       └── __init__.py            # Central configuration constants
│   ├── utils/                         # Shared utilities
│   │   ├── utils.py                   # YAML, pickle, numpy helpers
│   │   └── ml_utils/
│   │       ├── model/estimator.py     # NetworkModel inference wrapper
│   │       └── metric/classification_metric.py
│   ├── cloud/
│   │   └── s3_syncer.py               # AWS S3 artifact sync
│   ├── exceptions/
│   │   └── exception.py               # Custom exception with traceback
│   └── logging/
│       └── logger.py                  # Application logger
├── Network_data/
│   └── Dataset-Phising-Website.xlsx   # Raw dataset
├── data_schema/
│   └── schema.yaml                    # Expected column schema
├── final_model/
│   ├── model.pkl                      # Trained best model (~17 MB)
│   └── preprocessing.pkl              # Fitted KNN preprocessor (~5 MB)
├── artifacts/                         # Pipeline run artifacts
├── mlartifacts/                       # MLflow local artifact store
├── logs/                              # Application logs
├── predicted_output/                  # Batch prediction results
├── main.py                            # CLI entry point for training
├── app.py                             # FastAPI application
├── push_data.py                       # Excel → MongoDB ETL script
├── requirements.txt                   # Python dependencies
├── setup.py                           # Package setup
├── Dockerfile                         # Docker image definition
├── mlflow.db                          # Local MLflow tracking database
└── readme.md                          # Project documentation
```

---

## Tech Stack

| Category | Tool / Library |
|----------|---------------|
| Language | Python 3.8+ |
| ML | scikit-learn |
| Data Processing | pandas, NumPy |
| Experiment Tracking | MLflow, DagShub |
| Web Framework | FastAPI, Uvicorn |
| Database | MongoDB (via PyMongo) |
| Cloud Storage | AWS S3 |
| Containerisation | Docker |
| Configuration | python-dotenv, PyYAML |
| Serialisation | dill |

---

## Getting Started

### Prerequisites

- Python **3.8** or later
- A running **MongoDB** instance (local or [MongoDB Atlas](https://www.mongodb.com/atlas))
- (Optional) AWS account with S3 bucket for artifact syncing
- (Optional) [DagShub](https://dagshub.com) account for remote MLflow tracking

---

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/farehaaslam/network_security.git
cd network_security

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

### Environment Variables

Create a `.env` file in the project root:

```env
# MongoDB connection string (required)
MONGO_DB_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority

# AWS credentials (required only if S3 syncing is enabled)
AWS_ACCESS_KEY_ID=<your_access_key>
AWS_SECRET_ACCESS_KEY=<your_secret_key>
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_NAME=<your_s3_bucket_name>
```

> **Note**: Never commit your `.env` file to version control.

---

### Load Data into MongoDB

Before training, load the raw Excel dataset into MongoDB:

```bash
python push_data.py
```

This converts `Network_data/Dataset-Phising-Website.xlsx` → JSON records → MongoDB collection `network_data` inside the `Network_security` database.

---

## Usage

### Train the Model

**Option A — Via CLI:**
```bash
python main.py
```

**Option B — Via API (server must be running):**
```bash
curl -X GET http://localhost:8000/train
```

The training pipeline will:
1. Ingest data from MongoDB
2. Validate the schema and check for drift
3. Apply KNN imputation
4. Run GridSearchCV over five classifier families
5. Log all experiments to MLflow
6. Save the best model to `final_model/`
7. (Optional) Sync artifacts to AWS S3

---

### Run the FastAPI Server

```bash
python app.py
```

The API will be available at **http://localhost:8000**.

Interactive API documentation (Swagger UI): **http://localhost:8000/docs**

---

### Run with Docker

```bash
# Build the Docker image
docker build -t network-security-app .

# Run the container
docker run -p 8000:8000 --env-file .env network-security-app
```

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check — returns welcome message |
| `GET` | `/train` | Triggers the full training pipeline |
| `POST` | `/predict` | Accepts a CSV file and returns predictions |

### `POST /predict` — Batch Prediction

**Request** (multipart/form-data):

| Field | Type | Description |
|-------|------|-------------|
| `file` | `UploadFile` | CSV file with website feature columns |

**Example using curl:**
```bash
curl -X POST \
  http://localhost:8000/predict \
  -F "file=@path/to/input.csv"
```

**Response:**
- Status `200` with message `Prediction successful !!`
- Predictions are written to `predicted_output/output.csv`

**Input CSV format** — one row per website, 30 feature columns matching the schema in `data_schema/schema.yaml`. The `Result` column must **not** be included.

---

## Model Information

| Property | Value |
|----------|-------|
| Task | Binary Classification |
| Target variable | `Result` (1 = Phishing, -1 = Legitimate) |
| Minimum required accuracy | 60% |
| Preprocessing | KNN Imputer (`n_neighbors=3`) |
| Best model artifact | `final_model/model.pkl` |
| Preprocessor artifact | `final_model/preprocessing.pkl` |
| Experiment tracking | MLflow + DagShub (`farehaaslam/network_security`) |

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them: `git commit -m "Add your feature"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a **Pull Request** against the `main` branch

Please ensure your changes:
- Follow the existing code style
- Include appropriate logging using the project's logger
- Handle exceptions using `NetworkSecurityException`

---

## License

This project is open source and available under the [MIT License](LICENSE).
