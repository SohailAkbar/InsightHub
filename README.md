InsightHub- ML Powered Stock Analytics & Prediction API

InsightHub is a production-style FastAPI backend that provides stock
price analytics, machine learning based forecasting, model comparison,
drift detection, and prediction monitoring.

This project demonstrates how to design and structure a real-world ML
micro-service rather than just training a model in a notebook.

------------------------------------------------------------------------

OVERVIEW

InsightHub simulates a production ML pipeline:

-   Stores stock price history
-   Generates predictions using multiple ML models
-   Automatically selects the best-performing model
-   Tracks prediction accuracy
-   Detects model drift
-   Supports retraining workflows

The system follows clean backend architecture principles with separation
of API, business logic, and ML services.

------------------------------------------------------------------------

KEY FEATURES

Descriptive Analytics - Growth percentage calculation - 7-day moving
average - Volatility (standard deviation) - Historical trend insights

Machine Learning Prediction - Linear Regression - Random Forest
Regressor - Automatic model selection (based on MSE) - Rolling window
training (last 90 days) - Lag-based feature engineering

Model Comparison - Mean Squared Error (MSE) - R² Score comparison -
Performance benchmarking between models

Drift Detection - Calculates prediction error percentage - Flags model
drift if threshold exceeded - Configurable drift threshold

Prediction Monitoring - Stores predictions in database - Updates actual
values when new price data arrives - Tracks error percentage - Computes
mean prediction accuracy

Retraining Endpoint - Manual retraining support - Uses latest rolling
window data

------------------------------------------------------------------------

ARCHITECTURE

Project Structure:

app/ core/ Configuration models/ SQLAlchemy models schemas/ Pydantic
schemas services/ Business logic & ML logic routes/ API endpoints
database.py Database connection main.py Application entry point

Design Principles: - Separation of concerns - Config-driven
architecture - Service-layer ML logic - Database-backed monitoring

------------------------------------------------------------------------

TECH STACK

-   FastAPI
-   PostgreSQL
-   SQLAlchemy
-   Scikit-learn
-   NumPy
-   Uvicorn

------------------------------------------------------------------------

API ENDPOINTS

GET /health Health check POST /stocks Create stock GET /stocks List
stocks POST /prices Insert price GET /prices/{stock_id} Fetch price
history GET /analytics/{stock_id} Descriptive analytics GET
/predict/{stock_id} Generate next prediction GET
/model-compare/{stock_id} Compare ML models GET
/prediction-accuracy/{stock_id} Evaluate model accuracy GET
/drift-status/{stock_id} Detect model drift POST /retrain/{stock_id}
Retrain model

Swagger documentation: http://127.0.0.1:8000/docs

------------------------------------------------------------------------

INSTALLATION

1.  Clone repository

git clone cd insighthub-backend

2.  Create virtual environment

python3 -m venv venv source venv/bin/activate

3.  Install dependencies

pip install -r requirements.txt

4.  Configure environment variables

Create a .env file:

DATABASE_URL=postgresql://username:password@host:port/dbname

Important: Do NOT commit the .env file to GitHub.

5.  Run application

uvicorn app.main:app –reload

------------------------------------------------------------------------

HOW PREDICTION WORKS

1.  Fetch last 90 days of price history
2.  Create lag-based features
3.  Split into training and testing sets
4.  Train Linear Regression and Random Forest
5.  Compare MSE values
6.  Select best model
7.  Predict next closing price
8.  Store prediction in database
9.  Evaluate prediction once actual value arrives

------------------------------------------------------------------------

DRIFT DETECTION LOGIC

After each evaluated prediction:

-   Error percentage is calculated
-   If error exceeds threshold (default 10%), drift is flagged

This simulates monitoring used in real ML production systems.

------------------------------------------------------------------------

WHAT THIS PROJECT DEMONSTRATES

-   Production-style ML API design
-   Model evaluation and comparison
-   Monitoring and drift detection
-   Database-driven prediction tracking
-   Clean backend architecture
-   Configurable ML pipeline

This project bridges the gap between experimentation and deployable ML
systems.

------------------------------------------------------------------------

FUTURE IMPROVEMENTS

-   Model persistence using joblib
-   Automated scheduled retraining
-   Docker containerization
-   CI/CD integration
-   Cloud deployment (AWS / Render / Railway)
-   Integration with real market data APIs

------------------------------------------------------------------------

SECURITY PRACTICES

-   Environment-based configuration
-   No hardcoded secrets
-   .env excluded via .gitignore
-   Database credentials not committed

------------------------------------------------------------------------
