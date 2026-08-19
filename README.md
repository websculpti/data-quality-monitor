Data Quality Monitoring API

A beginner-friendly FastAPI-based data quality monitoring system that allows users to upload a dataset, analyze its quality, and generate a structured report.

The project is being built step-by-step to understand how a backend API, data-processing services, validation, testing, and AI-assisted explanations work together.

---

📌 Project Overview

Data quality is an important part of any data science or machine learning workflow.

Before using a dataset for analysis or training a model, we need to know:

- Are there missing values?
- Are there duplicate records?
- Are the data types correct?
- Are some columns almost entirely empty?
- Are there unusual or inconsistent values?
- How complete and usable is the dataset?

This project aims to automate these checks through a simple REST API.

Basic workflow

                User
                  |
                  | Upload CSV
                  v
            /upload endpoint
                  |
                  v
             Data Loader
                  |
                  v
              data/
                  |
                  | Run Analysis
                  v
            /analyze endpoint
                  |
                  v
          Data Quality Service
                  |
                  v
             Quality Metrics
                  |
                  | Generate Report
                  v
             Report Service
                  |
                  v
              reports/
                  |
                  v
             Final Report

The endpoints are logically connected, but each endpoint is triggered by a separate HTTP request.

---

🎯 Project Goals

The main goals of this project are to learn and implement:

- REST API development using FastAPI
- File uploading and handling
- Dataset processing using Pandas
- Input/output validation using Pydantic
- Separation of API routes and business logic
- Data quality analysis
- Report generation
- Logging
- Basic automated testing
- Optional LLM-based explanations of data quality issues

---

🏗️ Project Architecture

The project follows a simple layered architecture:

Client
  |
  v
Routes
  |
  v
Services
  |
  +------> Schemas
  |
  +------> Utils
  |
  v
Data / Reports

Main layers

Layer| Responsibility
"routes/"| Defines API endpoints
"services/"| Contains the actual business logic
"schemas/"| Defines and validates data structures
"utils/"| Shared configuration and utilities
"data/"| Stores uploaded datasets
"reports/"| Stores generated reports
"tests/"| Verifies that the application behaves correctly

---

📂 Project Structure

data-quality-monitor/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── upload.py
│   │   ├── analyze.py
│   │   ├── report.py
│   │   └── health.py
│   │
│   ├── services/
│   │   ├── data_loader.py
│   │   ├── data_quality.py
│   │   ├── report_generator.py
│   │   └── llm_explainer.py
│   │
│   ├── schemas/
│   │   ├── dataset_schema.py
│   │   └── report_schema.py
│   │
│   └── utils/
│       ├── config.py
│       └── logger.py
│
├── data/
│   └── uploaded datasets
│
├── reports/
│   └── generated reports
│
├── tests/
│   ├── test_upload.py
│   └── test_analyze.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md

---

🔄 How the System Works

1. Upload Dataset

The user sends a request to:

POST /upload

with a CSV file.

The request enters:

main.py
   ↓
routes/upload.py
   ↓
services/data_loader.py
   ↓
data/

The dataset is saved and information about it can be returned to the user.

Example response:

{
  "message": "Dataset uploaded successfully",
  "dataset_id": "customer_data"
}

---

2. Analyze Dataset

After uploading the dataset, the user sends another request:

POST /analyze

The analysis route calls the data quality service.

/analyze
    |
    v
analyze.py
    |
    v
data_loader.py
    |
    v
data_quality.py
    |
    v
quality metrics

The system can calculate metrics such as:

- Number of rows
- Number of columns
- Missing values
- Missing-value percentage
- Duplicate rows
- Number of unique values
- Data types
- Basic statistics
- Potential data quality issues

---

3. Generate Report

The analysis results are then used to create a structured report.

Quality Metrics
      |
      v
report_generator.py
      |
      v
reports/

The report can contain information such as:

{
  "dataset": "customer_data.csv",
  "rows": 1000,
  "columns": 12,
  "missing_values": {},
  "duplicate_rows": 5,
  "quality_score": 87
}

The exact report structure will evolve as the project is developed.

---

🤖 Optional AI Explanation

One planned component is:

services/llm_explainer.py

The purpose of this module is not to perform the actual data-quality calculations.

Those calculations will be done programmatically.

Instead, the LLM can take the detected issues and convert them into understandable explanations.

For example:

Detected:
age column has 38% missing values

The LLM could explain:

The age column contains a relatively high number of missing
values. Before using this column for analysis or machine
learning, consider investigating why the values are missing
and choosing an appropriate imputation strategy.

This keeps the responsibilities separate:

Pandas / Python
      |
      | Detect issues
      v
Data Quality Service
      |
      | Results
      v
LLM Explainer
      |
      | Human-readable explanation
      v
Final Report

---

🧩 Role of Each File

"main.py"

The entry point of the FastAPI application.

It is responsible for:

- Creating the FastAPI application
- Registering routes
- Starting the application

---

"routes/"

Contains the API endpoints.

"upload.py"

Handles dataset uploads.

POST /upload

"analyze.py"

Triggers dataset analysis.

POST /analyze

"report.py"

Provides the generated report.

GET /report

"health.py"

Provides a simple health-check endpoint.

GET /health

---

"services/"

Contains the main business logic.

"data_loader.py"

Responsible for loading and handling datasets.

Initially, the project will focus on CSV files.

Future support may include formats such as:

CSV
Excel
Parquet

"data_quality.py"

The main data-quality analysis engine.

It will calculate and identify issues such as:

Missing values
Duplicates
Data types
Unique values
Basic statistics
Potential outliers

"report_generator.py"

Converts the analysis results into a structured report.

"llm_explainer.py"

Optionally converts technical quality findings into natural-language explanations.

---

"schemas/"

Contains Pydantic models.

Schemas define what the application's input and output data should look like.

For example:

Dataset metadata
Report structure
API responses

Pydantic validation protects the API from incorrectly structured data.

---

"utils/"

Contains functionality shared by different parts of the application.

"config.py"

Stores application configuration such as:

Data directory
Report directory
Allowed file types
File size limits
Environment variables

"logger.py"

Provides logging so that we can understand what the application is doing.

Example:

Dataset uploaded
Analysis started
Analysis completed
Report generated

---

🧪 Testing

The "tests/" directory contains automated tests.

Testing has a different purpose from Pydantic validation.

Pydantic
    ↓
Validates incoming data

Tests
    ↓
Checks whether the application behaves correctly

For example, an upload test can verify that:

- A valid file can be uploaded
- The endpoint returns the expected status code
- The file is saved
- The response contains the expected information

The project will initially use simple tests rather than complex testing infrastructure.

---

🛠️ Tech Stack

Backend

- Python
- FastAPI
- Uvicorn

Data Processing

- Pandas

Validation

- Pydantic

Testing

- Pytest

Configuration

- Python dotenv

AI

- LLM API (optional / planned)

---

🚀 Getting Started

1. Clone the repository

git clone <your-repository-url>
cd data-quality-monitor

2. Create a virtual environment

Windows

python -m venv venv
venv\Scripts\activate

macOS / Linux

python3 -m venv venv
source venv/bin/activate

---

3. Install dependencies

pip install -r requirements.txt

---

4. Configure environment variables

Create a ".env" file in the root directory.

Example:

# Add API keys here when required
# LLM_API_KEY=your_api_key

Do not commit real API keys or secrets to GitHub.

---

5. Run the application

From the project root:

uvicorn app.main:app --reload

The API should then be available locally.

---

📖 API Workflow

The intended workflow is:

Step 1 — Upload

POST /upload

Upload the dataset.

Step 2 — Analyze

POST /analyze

Run the data-quality checks.

Step 3 — Report

GET /report

Retrieve the generated report.

Step 4 — Health Check

GET /health

Check whether the API is running.

---

🔗 Endpoint Relationship

The endpoints are separate HTTP requests, but they form one logical workflow.

                 ┌──────────────┐
                 │     User     │
                 └──────┬───────┘
                        │
                        │ POST /upload
                        ▼
                ┌───────────────┐
                │  upload.py    │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ data_loader.py│
                └───────┬───────┘
                        │
                        ▼
                     data/
                        │
                        │ POST /analyze
                        ▼
                ┌───────────────┐
                │  analyze.py   │
                └───────┬───────┘
                        │
                        ▼
              ┌───────────────────┐
              │ data_quality.py   │
              └─────────┬─────────┘
                        │
                        ▼
                  Quality Metrics
                        │
                        │ GET /report
                        ▼
              ┌───────────────────┐
              │ report_generator  │
              └─────────┬─────────┘
                        │
                        ▼
                    reports/
                        │
                        ▼
                     User

---

📈 Development Roadmap

This project is being developed incrementally.

Phase 1 — Project Setup

- [x] Create project structure
- [ ] Configure FastAPI
- [ ] Configure environment variables
- [ ] Add logging

Phase 2 — Dataset Upload

- [ ] Create upload endpoint
- [ ] Validate uploaded files
- [ ] Save datasets
- [ ] Return dataset metadata

Phase 3 — Data Quality Analysis

- [ ] Load uploaded dataset
- [ ] Check missing values
- [ ] Check duplicate rows
- [ ] Analyze data types
- [ ] Calculate unique-value statistics
- [ ] Add basic statistical checks
- [ ] Calculate an overall quality score

Phase 4 — Reporting

- [ ] Create report schema
- [ ] Generate structured reports
- [ ] Save reports
- [ ] Create report endpoint

Phase 5 — Testing

- [ ] Test upload functionality
- [ ] Test analysis functionality
- [ ] Test report generation
- [ ] Test invalid inputs

Phase 6 — AI Enhancement

- [ ] Add LLM integration
- [ ] Generate explanations for detected issues
- [ ] Add recommendations to reports

Phase 7 — Improvements

- [ ] Improve error handling
- [ ] Improve API documentation
- [ ] Add more file formats
- [ ] Improve data-quality checks

---

🎓 Learning Objectives

This project is primarily being developed as a learning project.

By completing it, the goal is to understand how a real application can be divided into smaller responsibilities:

API
 ↓
Routes
 ↓
Business Logic
 ↓
Data Processing
 ↓
Validation
 ↓
Reports
 ↓
Testing

Instead of putting everything inside one large Python file, the project separates responsibilities into modules that communicate with each other.

---

🔮 Future Improvements

Possible future additions include:

- Database-backed dataset management
- User authentication
- Background processing for large datasets
- Dashboard / frontend
- More advanced anomaly detection
- Data drift monitoring
- Dataset versioning
- Docker support
- Cloud deployment
- More advanced LLM-generated recommendations

These features are intentionally outside the initial scope so that the core workflow can be understood and implemented first.

---

📄 License

This project is currently intended for educational and learning purposes.
