# API Health Checker

![Tests](https://github.com/rimiify/API_health_checker/actions/workflows/main.yml/badge.svg)

A configurable Python-based API monitoring tool that checks REST API health, validates JSON responses, measures response performance, and stores historical monitoring data in SQLite.

The project is designed as a lightweight command-line monitoring utility with modular Python architecture, automated testing, structured configuration, logging, and continuous integration.

---

## 🚀 Features

* Monitor multiple REST API endpoints
* Measure HTTP status codes
* Measure API response time
* Measure response size
* Detect connection failures and request timeouts
* Parse JSON API responses
* Validate required response fields
* Validate expected data types
* Detect unexpected response fields as warnings
* Classify API health as:

  * `HEALTHY`
  * `DEGRADED`
  * `UNHEALTHY`
* Configure endpoints using JSON
* Validate endpoint configuration before execution
* Store monitoring history in SQLite
* View historical API statistics
* View recent monitoring checks
* Generate JSON health reports
* Maintain application logs
* Command-line interface using `argparse`
* Automated testing with `pytest`
* GitHub Actions continuous integration

---

## 🏗️ Architecture

```text
                    ┌─────────────────┐
                    │   CLI / main.py │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Config Loader   │
                    │ + Validation    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   API Client    │
                    │    requests     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Health Checker  │
                    │ Response Data   │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
      ┌───────────────┐             ┌───────────────┐
      │ Health        │             │ JSON          │
      │ Analyzer      │             │ Validator     │
      └───────┬───────┘             └───────┬───────┘
              │                             │
              └──────────────┬──────────────┘
                             ▼
                    ┌─────────────────┐
                    │ Monitoring      │
                    │ Record          │
                    └───────┬─────────┘
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
          ┌──────────────┐      ┌──────────────┐
          │   SQLite     │      │ JSON Report  │
          │   History    │      │              │
          └──────┬───────┘      └──────────────┘
                 │
                 ▼
          Historical Analytics
```

---

## 🛠️ Tech Stack

| Technology     | Purpose                       |
| -------------- | ----------------------------- |
| Python         | Core application              |
| Requests       | HTTP/API communication        |
| SQLite         | Historical monitoring storage |
| JSON           | Configuration and reports     |
| argparse       | Command-line interface        |
| pytest         | Automated testing             |
| GitHub Actions | Continuous integration        |
| dataclasses    | Structured application data   |

---

## 📁 Project Structure

```text
API_health_checker/
│
├── .github/
│   └── workflows/
│       └── main.yml
│
├── src/
│   ├── __init__.py
│   ├── api_client.py
│   ├── analyzer.py
│   ├── config_loader.py
│   ├── database.py
│   ├── health_checker.py
│   ├── history.py
│   ├── logger.py
│   ├── models.py
│   ├── reporter.py
│   └── validator.py
│
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_api_client.py
│   ├── test_config_loader.py
│   ├── test_database.py
│   ├── test_history.py
│   └── test_validator.py
│
├── config/
│   └── endpoints.json
│
├── data/
│   └── .gitkeep
│
├── logs/
│   └── .gitkeep
│
├── reports/
│   └── .gitkeep
│
├── main.py
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/rimiify/API_health_checker.git
cd API_health_checker
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the project

Install the application and development dependencies:

```bash
pip install -e ".[dev]"
```

---

## 🔧 Configuration

API endpoints are configured in:

```text
config/endpoints.json
```

Example:

```json
{
    "endpoints": [
        {
            "name": "Users API",
            "url": "https://jsonplaceholder.typicode.com/users/1",
            "expected_fields": [
                "id",
                "name",
                "username",
                "email"
            ],
            "expected_types": {
                "id": "int",
                "name": "str",
                "username": "str",
                "email": "str"
            },
            "max_response_time": 2.0
        }
    ]
}
```

### Configuration fields

| Field               | Description                                    |
| ------------------- | ---------------------------------------------- |
| `name`              | Human-readable API name                        |
| `url`               | API endpoint URL                               |
| `expected_fields`   | Required fields expected in the JSON response  |
| `expected_types`    | Expected Python data types for response fields |
| `max_response_time` | Maximum acceptable response time in seconds    |

The configuration loader validates the configuration before the monitoring process begins.

Invalid configurations such as missing fields, unsupported data types, empty endpoint names, and invalid response-time thresholds are rejected with descriptive errors.

---

## ▶️ Usage

### Check all configured APIs

```bash
python main.py --all
```

The application checks every endpoint configured in `config/endpoints.json`.

---

### View monitoring history

```bash
python main.py --history
```

Displays historical statistics including:

* Total checks
* Average response time
* Slowest response
* Healthy checks
* Degraded checks
* Unhealthy checks

---

### View history for a specific API

```bash
python main.py --history --endpoint "Users API"
```

---

### View recent checks

```bash
python main.py --history --recent 5
```

Displays the five most recent monitoring records.

---

### View recent checks for a specific API

```bash
python main.py --history --endpoint "Users API" --recent 5
```

---

## 📊 Health Classification

The health analyzer evaluates API reachability, HTTP status codes, and response latency.

### `HEALTHY`

An API is classified as healthy when:

* The endpoint is reachable
* It does not return an error status
* Response time is within the configured threshold

### `DEGRADED`

An API is classified as degraded when it is reachable but has an issue such as:

* HTTP `4xx` response
* Response time exceeding the configured threshold

### `UNHEALTHY`

An API is classified as unhealthy when:

* The request cannot reach the endpoint
* A timeout or connection failure occurs
* The server returns an HTTP `5xx` response

---

## 🔍 Response Validation

The project validates JSON API responses against endpoint-specific expectations.

For example:

```json
{
    "expected_fields": [
        "id",
        "name",
        "email"
    ],
    "expected_types": {
        "id": "int",
        "name": "str",
        "email": "str"
    }
}
```

The validator checks:

### Required fields

Detects missing expected fields.

### Data types

Detects fields whose actual type does not match the configured type.

For example:

```text
Expected: int
Actual:   str
```

### Unexpected fields

Additional fields are reported as warnings rather than failures.

This allows APIs to evolve without treating every newly introduced response field as an error.

---

## 🗄️ Historical Monitoring

Each completed health check is stored in a local SQLite database.

Database location:

```text
data/api_health.db
```

Stored information includes:

* Timestamp
* API name
* URL
* HTTP status code
* Response time
* Response size
* Reachability
* Health classification

This allows the application to analyze historical API behavior rather than only reporting the current request.

---

## 📄 Reports

After running health checks, a JSON report is generated at:

```text
reports/health_report.json
```

The report contains:

* Report generation timestamp
* Total APIs checked
* Number of healthy APIs
* Number of degraded APIs
* Number of unhealthy APIs
* Individual API results
* Validation results where applicable

---

## 📝 Logging

Application events are written to:

```text
logs/api_health.log
```

The logger records events such as:

* Health check started
* Health check completed
* API health classification

Generated logs and local database files are excluded from version control using `.gitignore`.

---

## 🧪 Testing

The project uses `pytest` for automated testing.

Run the complete test suite:

```bash
pytest
```

The current test suite contains **30 automated tests** covering:

* Successful API requests
* Request timeouts
* Connection errors
* General request failures
* API health classification
* JSON field validation
* Data type validation
* Unexpected response fields
* Configuration validation
* Invalid configuration handling
* SQLite database initialization
* Health check persistence
* Historical statistics
* Recent monitoring queries

External API requests are mocked in the tests where appropriate so that tests remain deterministic and do not depend on live network responses.

---

## 🔄 Continuous Integration

GitHub Actions automatically runs the test suite when code is pushed to the repository or submitted through a pull request.

![Tests](https://github.com/rimiify/API_health_checker/actions/workflows/main.yml/badge.svg)

The CI pipeline performs the following steps:

```text
Push / Pull Request
        │
        ▼
Checkout Repository
        │
        ▼
Set Up Python
        │
        ▼
Install Dependencies
        │
        ▼
Run pytest
        │
        ▼
Build Status
```

A green status indicates that the automated test suite completed successfully.

---

## 🧠 Engineering Concepts Demonstrated

This project demonstrates practical Python development concepts including:

* Python modular architecture
* Object-oriented data modeling
* Dataclasses
* Type hints
* REST API integration
* HTTP error handling
* Exception handling
* JSON processing
* Configuration management
* Configuration validation
* SQLite database operations
* SQL queries
* Command-line application development
* Automated testing
* Mocking external API requests
* Logging
* Git version control
* GitHub Actions continuous integration

---

## 🔮 Future Improvements

Potential future improvements include:

* Configurable retry mechanisms
* Scheduled monitoring
* Performance trend analysis
* Response anomaly detection
* Additional database analytics
* Test coverage reporting
* More advanced CLI filtering
* Configurable request methods such as POST and PUT
* Support for authentication headers

---

## 📌 Project Status

**Version:** `1.0.0`

The core monitoring, response validation, historical persistence, CLI reporting, automated testing, and continuous integration functionality is implemented.

---

## 👩‍💻 Author

**Rimjhim**

Built as a practical Python engineering project focused on API integration, automation, testing, and maintainable software design.
