"""
Model Evaluation Service

Used for:
- Model comparison endpoint
- Error aggregation
"""

import numpy as np
from statistics import mean
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


def evaluate_models(prices):
    if len(prices) < 5:
        return None

    values = [p.close_price for p in prices]

    X = np.arange(len(values)).reshape(-1, 1)
    y = np.array(values)

    split = int(len(X) * 0.8)

    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)

    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)

    return {
        "LinearRegression": {
            "MSE": round(mean_squared_error(y_test, lr_pred), 4),
            "R2_Score": round(r2_score(y_test, lr_pred), 4),
        },
        "RandomForest": {
            "MSE": round(mean_squared_error(y_test, rf_pred), 4),
            "R2_Score": round(r2_score(y_test, rf_pred), 4),
        },
    }


def calculate_mean_error(predictions):
    evaluated = [
        p.error_percentage
        for p in predictions
        if p.error_percentage is not None
    ]

    if not evaluated:
        return None

    return round(mean(evaluated), 3)