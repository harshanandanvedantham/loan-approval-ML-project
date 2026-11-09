# LOANWISE

Machine Learning Based Loan Approval Prediction System

LOANWISE is an educational web application that predicts whether a loan application is likely to be classified as **Approved** or **Rejected** using a machine learning model.

> **Important:** LOANWISE is an academic/educational project. Its output is a machine learning prediction, **not** an official bank decision, loan offer, financial advice, or guarantee of approval. Do not use it to make real lending decisions.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Data Preparation and Model Training](#data-preparation-and-model-training)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Model Explainability](#model-explainability)
- [Troubleshooting](#troubleshooting)
- [Public Demo with Cloudflare Tunnel](#public-demo-with-cloudflare-tunnel)
- [Limitations](#limitations)
- [Project Information](#project-information)

## Features

- User registration and login
- Submission of loan and financial details
- Model-generated prediction (Approved / Rejected) with class probability
- Explanation of the prediction using SHAP and rule-based observations
- Application history and profile pages (where configured)

## Technology Stack

- **Backend:** Python, Flask
- **Database:** MySQL
- **Machine learning:** pandas, NumPy, scikit-learn
- **Explainability:** SHAP
- **Frontend:** HTML, CSS, JavaScript

## Project Structure

The project directory should contain the following. Optional files may differ depending on your local version.

```text
loanwise/
├── app.py
├── database.py
├── data_cleaning.py
├── train_model.py
├── explainability.py
├── test_model.py
├── test_model_cases.py          # optional
├── requirements.txt             # recommended
├── README.md
│
├── dataset/
│   └── cleaned_loan_dataset.csv
│
├── models/
│   ├── loan_approval_model.pkl
│   └── model_info.json
│
├── templates/
│   ├── application.html
│   ├── dashboard.html
│   ├── history.html
│   ├── login.html
│   ├── profile.html
│   ├── register.html
│   └── result.html
│
└── static/
    └── css/
        └── style.css
```

The trained model file must be available at the path expected by `explainability.py`. The cleaned dataset is used by the training workflow.

## System Requirements

- Python 3.10 or a compatible version supported by the installed packages
- MySQL Server 8.x (or a compatible version)
- A modern web browser
- Internet connection for the initial package installation
- Windows, macOS, or Linux

Verify your tools:

```bash
python --version      # or python3 --version
python -m pip --version
```

## Installation

### 1. Clone or download the project

```bash
cd path/to/loanwise
```

### 2. Create and activate a virtual environment

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, allow scripts for the current session only and try again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 3. Install dependencies

If a `requirements.txt` file is provided:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Otherwise, install the core packages manually:

```bash
python -m pip install --upgrade pip
pip install Flask pandas numpy scikit-learn shap mysql-connector-python
```

Install any additional packages your code imports.

## Database Setup

1. Start your MySQL Server.
2. Open MySQL Workbench or the MySQL command-line client.
3. Create the database and tables:

```sql
CREATE DATABASE IF NOT EXISTS loanwise_db;
USE loanwise_db;

CREATE TABLE IF NOT EXISTS users (
    user_id       INT AUTO_INCREMENT PRIMARY KEY,
    full_name     VARCHAR(100),
    email         VARCHAR(150) UNIQUE,
    password_hash VARCHAR(255),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS loan_applications (
    application_id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id                  INT NOT NULL,
    no_of_dependents         INT NOT NULL,
    education                VARCHAR(30) NOT NULL,
    self_employed            VARCHAR(10) NOT NULL,
    income_annum             BIGINT NOT NULL,
    loan_amount              BIGINT NOT NULL,
    loan_term                INT NOT NULL,
    cibil_score              INT NOT NULL,
    residential_assets_value BIGINT NOT NULL,
    commercial_assets_value  BIGINT NOT NULL,
    luxury_assets_value      BIGINT NOT NULL,
    bank_asset_value         BIGINT NOT NULL,
    predicted_status         VARCHAR(20) NOT NULL,
    predicted_probability    DECIMAL(7,3) NOT NULL,
    model_name               VARCHAR(100),
    model_version            VARCHAR(50),
    explanation              JSON,
    created_at               TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_application_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
);
```

The database name, table names, and column names must match the SQL queries in `app.py` and `database.py`. If the tables already exist, verify their structure instead of recreating them.

## Configuration

`database.py` reads its settings from environment variables. The defaults are host `localhost` and database `loanwise_db`.

| Variable | Description | Example |
| --- | --- | --- |
| `MYSQL_HOST` | MySQL server host | `localhost` |
| `MYSQL_PORT` | MySQL server port | `3306` |
| `MYSQL_USER` | MySQL username | `root` |
| `MYSQL_PASSWORD` | MySQL password | *(your password)* |
| `MYSQL_DATABASE` | Database name | `loanwise_db` |
| `FLASK_SECRET_KEY` | Secret key for session signing | *(a long random string)* |

**macOS / Linux:**

```bash
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD='your_mysql_password'
export MYSQL_DATABASE=loanwise_db
export FLASK_SECRET_KEY='replace-with-a-long-random-secret'
```

**Windows (PowerShell):**

```powershell
$env:MYSQL_HOST="localhost"
$env:MYSQL_PORT="3306"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="your_mysql_password"
$env:MYSQL_DATABASE="loanwise_db"
$env:FLASK_SECRET_KEY="replace-with-a-long-random-secret"
```

These variables apply only to the current terminal session. Set them again in new terminals, or configure them persistently through your operating system.

> **Security:** Never commit passwords or secret keys to version control. Use environment variables or a local `.env` file that is listed in `.gitignore`.

## Data Preparation and Model Training

**Expected cleaned dataset:** `dataset/cleaned_loan_dataset.csv`

**Input features:**

- `no_of_dependents`
- `education`
- `self_employed`
- `income_annum`
- `loan_amount`
- `loan_term`
- `cibil_score`
- `residential_assets_value`
- `commercial_assets_value`
- `luxury_assets_value`
- `bank_asset_value`

**Target column:** `loan_status`

The `loan_id` column is excluded from the model features.

To regenerate the cleaned dataset:

```bash
python data_cleaning.py
```

To train and save the model:

```bash
python train_model.py
```

The training script compares candidate classifiers using cross-validation and saves the selected model and its metadata to `models/`.

If trained model files are already provided and you only want to run the web application, you do not need to retrain. Just make sure the model file and metadata exist at the locations expected by `explainability.py`.

## Running the Application

Before starting, confirm that:

- MySQL Server is running
- `loanwise_db` and its tables exist
- The virtual environment is activated
- The environment variables are set
- The trained model file is present

From the project directory:

```bash
python app.py
```

Open your browser and go to:

```
http://127.0.0.1:5000/
```

**Typical workflow:**

1. Register a user account.
2. Log in.
3. Open the new loan application form.
4. Enter the personal, financial, and asset information.
5. Submit the application.
6. View the predicted status and explanation.
7. Visit the history and profile pages, if configured.

To stop the server, press `CTRL+C` in the terminal running `app.py`.

## Testing

Run the model test script:

```bash
python test_model.py
```

If the additional test-case script is present:

```bash
python test_model_cases.py
```

The test-case script checks that representative valid inputs are accepted, that a known model class is returned, and that probabilities form a valid distribution.

Good test coverage includes:

- High and low CIBIL score inputs
- Varied income and loan amount combinations
- Graduate and Not Graduate values
- Self-employed and not self-employed values
- Zero and non-zero asset values
- Minimum and maximum allowed input values
- Invalid or missing form inputs at the web application level

A successful prediction call confirms that the model runs. It does **not** prove that any individual prediction is correct.

## Model Explainability

The project uses SHAP-based explanations along with rule-based messages. An explanation may include:

- The predicted class
- The model-reported class probability
- Features with positive SHAP contributions
- Features with negative SHAP contributions
- Rule-based observations, such as CIBIL score and loan-to-income ratio

SHAP values show how features contributed to the model's output for a specific prediction. They do not prove causation and should not be treated as approval or rejection rules.

The displayed probability is the model's predicted probability. It should not be described as calibrated confidence unless calibration has been evaluated separately.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| **MySQL connection error** | MySQL is running; `MYSQL_*` variables are correct; `loanwise_db` exists; required tables and columns exist |
| **`ModuleNotFoundError`** | The virtual environment is active; install the missing package with `pip`; or run `pip install -r requirements.txt` |
| **Model file not found** | `models/loan_approval_model.pkl` exists; the path in `explainability.py` is correct; run `train_model.py` if needed |
| **Dataset file not found** | `dataset/` contains the expected CSV; the path used in `data_cleaning.py` or `train_model.py` is correct |
| **`TemplateNotFound`** | HTML files are inside `templates/`; `render_template()` uses the exact filename |
| **CSS not loading** | File is at `static/css/style.css`; the template uses `{{ url_for('static', filename='css/style.css') }}`; hard-refresh the browser (`Ctrl+F5` on Windows/Linux, `Cmd+Shift+R` on macOS) |
| **Port 5000 already in use** | Stop the other process, or run Flask on a different port |

## Public Demo with Cloudflare Tunnel

A Cloudflare Quick Tunnel can temporarily expose your local app through a public `trycloudflare.com` URL. It is suitable for classroom or project demonstrations, **not** for production.

1. Start Flask and confirm that `http://127.0.0.1:5000/` works.
2. Install `cloudflared` following Cloudflare's official instructions.
3. In a second terminal, run:

   ```bash
   cloudflared tunnel --url http://localhost:5000
   ```

4. Open the temporary HTTPS URL printed in the terminal.

Keep both Flask and `cloudflared` running during the demo. The URL changes each time a new Quick Tunnel is created.

**Security precautions:**

- Do not run Flask with `debug=True` when the app is publicly reachable.
- Do not expose MySQL port 3306 to the internet.
- Do not use real or sensitive financial data in a public demo.
- Protect database credentials and the Flask secret key.
- Stop the tunnel when the demo is over.

For a permanent deployment, use a production hosting environment, a production WSGI server (such as Gunicorn), secure environment variables, HTTPS, and a properly secured database.

## Limitations

- Predictions depend on the quality and representativeness of the training data.
- Strong test metrics do not guarantee similar performance on real-world applications.
- The dataset may not capture the full complexity of actual lending decisions.
- LOANWISE is not connected to any bank's official approval process.
- Predicted probabilities are not guaranteed to be calibrated.

## Project Information

| | |
| --- | --- |
| **Project name** | LOANWISE |
| **Project type** | Machine learning based loan approval prediction |
| **Web framework** | Flask |
| **Database** | MySQL |
| **ML tools** | Python, pandas, scikit-learn, SHAP |
