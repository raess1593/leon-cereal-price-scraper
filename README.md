# 🌾 León Cereal Price Predictor: Agricultural AI

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-orange)

## 📌 Project Purpose
An *End-to-End* Machine Learning system designed to help farmers predict the price fluctuations of cereals (wheat, barley, corn) at the local agricultural market (Lonja de León). 

This project demonstrates the full lifecycle of an ML model (core MLOps), going from raw data extraction to a fully containerized production deployment.

## 🏗️ Architecture & Tech Stack
The pipeline consists of 5 main modules:
1. **Web Scraping:** `pandas`, `requests`, and `BeautifulSoup` to extract weekly historical price data.
2. **Database:** SQLite managed through the `SQLAlchemy` ORM.
3. **ML Modeling:** Tree-based models (`scikit-learn`, Random Forest/XGBoost) for time-series forecasting.
4. **Experiment Tracking:** `MLflow` for logging hyperparameters and model performance metrics.
5. **Deployment (Serving):** RESTful API built with `FastAPI` and containerized using `Docker`.

## 📂 Project Structure (MVP)
```text
leon-ceral-price-AI/
├── data/                 # Local databases (SQLite) and raw CSVs
├── notebooks/            # Jupyter notebooks for EDA and sandbox testing
├── src/                  # Production source code
│   ├── scraper/          # Data extraction scripts
│   ├── database/         # SQLAlchemy models and DB configuration
│   ├── ml/               # Model training and MLflow integration
│   └── api/              # FastAPI endpoints
├── .env.example          # Environment variables template
├── docker-compose.yml    # Container orchestration
├── Dockerfile            # API build recipe
├── requirements.txt      # Project dependencies
└── README.md
