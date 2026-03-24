# 🔐 Network Security — Phishing Website Detection System

A production-ready end-to-end machine learning system for detecting phishing websites. The project classifies websites as **legitimate** or **phishing** based on 31 URL and website-behaviour features, and exposes predictions through a REST API backed by an automated training pipeline, MLflow experiment tracking, and AWS CI/CD deployment.

---

## 📑 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
  - [1. Load Data into MongoDB](#1-load-data-into-mongodb)
  - [2. Run the Training Pipeline](#2-run-the-training-pipeline)
  - [3. Start the REST API](#3-start-the-rest-api)
  - [4. Run with Docker](#4-run-with-docker)
- [API Reference](#api-reference)
- [ML Pipeline Details](#ml-pipeline-details)
- [CI/CD Deployment](#cicd-deployment)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Phishing attacks remain one of the most common and damaging cyber threats, tricking users into revealing sensitive credentials by mimicking legitimate websites. This project builds a **machine learning classifier** trained on labelled phishing-website features to detect such attacks automatically.

The system follows a modular, production-grade architecture:

1. Raw data is ingested from **MongoDB**.
2. Data quality and schema are validated (including **drift detection**).
3. Features are engineered and preprocessed with a **KNN imputation** pipeline.
4. Five candidate classifiers are trained simultaneously using **GridSearchCV**, and the best model is selected.
5. All experiments are logged to **MLflow** (via DagsHub).
6. The trained model is served through a **FastAPI** application and optionally stored on **AWS S3**.
7. A **GitHub Actions** workflow automatically builds, pushes, and deploys the containerised app to **AWS ECR / EC2**.

---

## Features

- ✅ **Automated ML Pipeline** — data ingestion → validation → transformation → training in one command  
- ✅ **Data Drift Detection** — Kolmogorov–Smirnov test flags distribution shifts between train and test sets  
- ✅ **Multi-model Comparison** — Random Forest, Gradient Boosting, AdaBoost, Logistic Regression, Decision Tree  
- ✅ **Hyperparameter Tuning** — GridSearchCV over each model  
- ✅ **Experiment Tracking** — MLflow metrics (F1, precision, recall) stored on DagsHub  
- ✅ **REST API** — FastAPI endpoints for training and batch prediction  
- ✅ **Batch Prediction** — upload a CSV and receive predictions  
- ✅ **Docker Support** — fully containerised application  
- ✅ **CI/CD to AWS** — GitHub Actions pipeline to ECR + EC2  
- ✅ **Cloud Storage** — AWS S3 artifact sync  
- ✅ **Structured Logging** — timestamped log files for every run  
- ✅ **Custom Exception Handling** — file-name and line-number aware errors  

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Sources                             │
│  Excel Dataset ──► push_data.py ──► MongoDB (feature store)     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Training Pipeline                            │
│                                                                  │
│  DataIngestion ──► DataValidation ──► DataTransformation         │
│       │                │                      │                  │
│  Reads MongoDB    Schema check +         KNN Imputation          │
│  80/20 split      Drift detection        Preprocessor pkl        │
│                                                 │                │
│                                          ModelTrainer            │
│                                     GridSearchCV (5 models)      │
│                                     Best model ──► final_model/  │
│                                     Metrics ──► MLflow           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                         FastAPI App                              │
│                                                                  │
│  GET  /        ─── Health check                                  │
│  GET  /train   ─── Trigger training pipeline                     │
│  POST /predict ─── Upload CSV ──► Batch predictions              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  CI/CD & Cloud Infrastructure                    │
│                                                                  │
│  GitHub Actions ──► Docker Build ──► AWS ECR ──► AWS EC2         │
│                                  └──► AWS S3 (artifacts/models)  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Dataset

| Property | Value |
|---|---|
| **Source** | `Network_data/Dataset-Phising-Website.xlsx` |
| **Rows** | ~11,000 labelled website records |
| **Target column** | `Result` (`-1` = phishing, `1` = legitimate) |
| **Feature count** | 31 binary/integer features |
| **Schema** | `data_schema/schema.yaml` |

### Feature List

> **Note:** Feature names below match the original dataset column names exactly, including any unconventional spellings (e.g. `Shortining_Service`, `popUpWidnow`).

| Feature | Description |
|---|---|
| `having_IP_Address` | URL uses an IP address instead of a domain name |
| `URL_Length` | Length of the URL |
| `Shortining_Service` | URL shortened using a service (e.g., bit.ly) |
| `having_At_Symbol` | `@` symbol present in URL |
| `double_slash_redirecting` | `//` appears after the protocol |
| `Prefix_Suffix` | `-` used in domain name |
| `having_Sub_Domain` | Number of sub-domains |
| `SSLfinal_State` | HTTPS certificate status |
| `Domain_registeration_length` | Domain registration period |
| `Favicon` | Favicon loaded from external domain |
| `port` | Non-standard port used |
| `HTTPS_token` | "https" token appears in domain part of URL |
| `Request_URL` | Percentage of external request URLs |
| `URL_of_Anchor` | Percentage of anchor tags linking externally |
| `Links_in_tags` | Links in `<meta>`, `<script>`, `<link>` tags |
| `SFH` | Server Form Handler destination |
| `Submitting_to_email` | Form submits data via `mailto:` |
| `Abnormal_URL` | Host name not present in URL |
| `Redirect` | Number of redirects |
| `on_mouseover` | Status bar changed on mouse-over |
| `RightClick` | Right-click disabled |
| `popUpWidnow` | Pop-up window contains text field |
| `Iframe` | `<iframe>` tag present |
| `age_of_domain` | Age of the domain |
| `DNSRecord` | DNS record available |
| `web_traffic` | Website traffic ranking |
| `Page_Rank` | Google PageRank |
| `Google_Index` | Website indexed by Google |
| `Links_pointing_to_page` | Number of links pointing to the page |
| `Statistical_report` | Host appears in top phishing IPs/domains list |

---

## Project Structure

```
network_security/
├── .github/
│   └── workflows/
│       └── main.yml              # GitHub Actions CI/CD pipeline
├── Network_security/             # Main Python package
│   ├── cloud/
│   │   └── s3_syncer.py          # AWS S3 artifact synchronisation
│   ├── components/               # Pipeline stage implementations
│   │   ├── data_ingestion.py     # MongoDB reader + train/test split
│   │   ├── data_validation.py    # Schema & drift validation
│   │   ├── data_transformation.py# KNN imputation & preprocessing
│   │   └── model_trainer.py      # Multi-model training + MLflow logging
│   ├── constants/
│   │   └── training_pipeline/    # Pipeline configuration constants
│   ├── entity/
│   │   ├── artifact_entity.py    # Pipeline output data classes
│   │   └── config_entity.py      # Pipeline configuration data classes
│   ├── exceptions/
│   │   └── exception.py          # NetworkSecurityException
│   ├── logging/
│   │   └── logger.py             # Structured file logging
│   ├── pipelines/
│   │   ├── training_pipeline.py  # Orchestrates full training workflow
│   │   └── batch_prediction.py   # Inference pipeline
│   └── utils/
│       ├── ml_utils/
│       │   ├── metric/           # Classification metric helpers
│       │   └── model/            # NetworkModel estimator wrapper
│       └── utils.py              # YAML I/O, pickle, GridSearch helpers
├── Network_data/
│   └── Dataset-Phising-Website.xlsx  # Raw labelled dataset
├── data_schema/
│   └── schema.yaml               # Column types & numeric column list
├── final_model/                  # Persisted artefacts
│   ├── model.pkl                 # Best trained classifier
│   └── preprocessing.pkl         # Fitted preprocessor pipeline
├── artifacts/                    # Per-run training artefacts
├── logs/                         # Timestamped log files
├── predicted_output/
│   └── output.csv                # Latest batch prediction results
├── app.py                        # FastAPI application entry point
├── main.py                       # CLI training entry point
├── push_data.py                  # ETL: Excel → MongoDB
├── Dockerfile                    # Container definition
├── requirements.txt              # Python dependencies
└── setup.py                      # Package installation
```

---

## Technologies Used

| Category | Tools / Libraries |
|---|---|
| **Language** | Python 3.x |
| **ML / Data** | scikit-learn, pandas, numpy |
| **Experiment Tracking** | MLflow, DagsHub |
| **Web Framework** | FastAPI, Uvicorn |
| **Database** | MongoDB (pymongo) |
| **Serialisation** | dill, pickle |
| **Cloud** | AWS S3 (boto3), AWS ECR, AWS EC2 |
| **Containerisation** | Docker |
| **CI/CD** | GitHub Actions |
| **Misc** | python-dotenv, pyaml, openpyxl |

---

## Installation & Setup

### Prerequisites

- Python 3.8+
- MongoDB Atlas account (or local MongoDB instance)
- AWS account (for S3, ECR, EC2 — optional for local development)

### 1. Clone the Repository

```bash
git clone https://github.com/farehaaslam/network_security.git
cd network_security
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
MONGO_DB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
S3_BUCKET_NAME=your-s3-bucket-name
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
```

> ⚠️ Never commit the `.env` file to version control.

---

## Usage

### 1. Load Data into MongoDB

The raw Excel dataset must be imported into MongoDB before training:

```bash
python push_data.py
```

This reads `Network_data/Dataset-Phising-Website.xlsx`, converts each row to a JSON document, and inserts the records into the configured MongoDB collection.

---

### 2. Run the Training Pipeline

```bash
python main.py
```

This triggers the complete training pipeline in sequence:

```
DataIngestion → DataValidation → DataTransformation → ModelTrainer
```

Artefacts are written to `artifacts/{timestamp}/` and the best model is saved to `final_model/`.

---

### 3. Start the REST API

```bash
python app.py
```

The server starts at `http://localhost:8000`. See [API Reference](#api-reference) for endpoint details.

---

### 4. Run with Docker

```bash
# Build the image
docker build -t network-security .

# Run the container
docker run -d -p 8000:8000 \
  -e MONGO_DB_URI="your_mongodb_uri" \
  -e S3_BUCKET_NAME="your_s3_bucket" \
  -e AWS_ACCESS_KEY_ID="your_key" \
  -e AWS_SECRET_ACCESS_KEY="your_secret" \
  -e AWS_REGION="us-east-1" \
  network-security
```

Access the API at `http://localhost:8000`.

---

## API Reference

### `GET /`

Health check endpoint.

**Response:**
```
200 OK
Welcome to Network Security API !!
```

---

### `GET /train`

Triggers the full training pipeline on the server.

**Response:**
```
200 OK
Training successful !!
```

> ⚠️ This is a long-running operation. Ensure MongoDB credentials are configured on the server.

---

### `POST /predict`

Accepts a CSV file and returns batch predictions.

**Request:**
```bash
curl -X POST \
  http://localhost:8000/predict \
  -F "file=@/path/to/your/data.csv"
```

**CSV format:** same columns as the training data (without the `Result` column).

**Response:**
```
200 OK
Prediction successful !!
```

Predictions are written to `predicted_output/output.csv` on the server.

---

## ML Pipeline Details

### Data Ingestion

- Reads records from the MongoDB collection specified by `DATA_INGESTION_COLLECTION_NAME`
- Exports a full feature store CSV to `artifacts/{ts}/data_ingestion/feature_store/`
- Performs an **80 / 20 train–test split** and saves both CSVs

### Data Validation

- Validates that all expected columns (from `data_schema/schema.yaml`) are present
- Checks column data types
- Runs a **Kolmogorov–Smirnov test** on each numeric feature to detect data drift
- Generates a YAML drift report under `artifacts/{ts}/data_validation/`

### Data Transformation

- Applies **KNN imputation** (`k=3`) to handle missing values
- Wraps the imputer in a scikit-learn `Pipeline` object
- Saves the fitted preprocessor to `final_model/preprocessing.pkl`

### Model Training

Five models are evaluated using **GridSearchCV** with cross-validation:

| Model | Key Hyperparameters Tuned |
|---|---|
| Random Forest | `n_estimators`, `max_depth`, `min_samples_split` |
| Gradient Boosting | `n_estimators`, `learning_rate`, `max_depth` |
| AdaBoost | `n_estimators`, `learning_rate` |
| Logistic Regression | `C`, `solver` |
| Decision Tree | `max_depth`, `criterion` |

The model with the **highest F1 score** on the test set is selected and saved as `final_model/model.pkl`. All metrics (F1, precision, recall) for every model are logged to **MLflow**.

---

## CI/CD Deployment

The `.github/workflows/main.yml` pipeline runs on every push to the `main` branch and consists of three stages:

```
1. Integration  ─── Linting & unit tests (if present)
2. Build        ─── Docker image build → push to AWS ECR
3. Deploy       ─── Pull latest image on EC2 self-hosted runner & restart
```

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |
| `AWS_REGION` | AWS region (e.g., `us-east-1`) |
| `ECR_REPOSITORY_NAME` | Name of the ECR repository |
| `AWS_ECR_LOGIN_URI` | ECR login URI (e.g., `<account_id>.dkr.ecr.<region>.amazonaws.com`) |

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `MONGO_DB_URI` | ✅ | MongoDB connection string |
| `S3_BUCKET_NAME` | ✅ (cloud) | AWS S3 bucket for artefact storage |
| `AWS_ACCESS_KEY_ID` | ✅ (cloud) | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | ✅ (cloud) | AWS IAM secret access key |
| `AWS_REGION` | ✅ (cloud) | AWS region |

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Commit your changes**: `git commit -m "feat: describe your change"`
4. **Push to your fork**: `git push origin feature/your-feature-name`
5. **Open a Pull Request** against the `main` branch

Please ensure your code follows the existing project conventions and all existing functionality continues to work.

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

*Built by [Fareha Aslam](https://github.com/farehaaslam)*
