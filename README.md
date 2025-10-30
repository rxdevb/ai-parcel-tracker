# AI Parcel Tracker: Courier Identification Microservice

This document serves as the official project guide for the **AI Parcel Tracker**, a Python microservice designed for identifying parcel couriers. The core functionality relies on a supervised Machine Learning model to determine the service provider based on the format and length of a tracking number.

The service is engineered for **containerization** (Docker) and implements architectural best practices, including robust dependency checks.

## Architecture and Core Technologies

* **API Framework:** Flask (used for a lightweight, scalable REST API layer).
* **Machine Learning:** Scikit-learn (Decision Tree Classifier is used for classification).
* **Data Handling:** Pandas (for data loading and feature engineering).
* **Database Resilience:** The service utilizes the `app.py` script and the `psycopg2` library to perform connection retries, ensuring stable startup when the PostgreSQL database is initializing.
* **Code Quality:** All code adheres to PEP 484 standards by utilizing **Type Hints** for improved maintainability and static code analysis.

## Setup and Installation

### Prerequisites

* Python 3.8+
* Virtual Environment (recommended)

### Installation Steps

Clone the repository and install dependencies from the `requirements.txt` file.

```bash
git clone [https://github.com/rxdevb/ai-parcel-tracker.git](https://github.com/rxdevb/ai-parcel-tracker.git)
cd ai-parcel-tracker

# Create and activate the virtual environment
python3 -m venv venv
source venv/bin/activate 

# Install required Python packages
pip install -r requirements.txt


