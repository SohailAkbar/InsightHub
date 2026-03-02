"""
Prediction Service

Handles:
- Lag feature engineering
- Rolling window training
- Model comparison (LR vs RF)
- Next price forecasting
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

from app.core.config import ROLLING_WINDOW_DAYS, LAG


def _create_lag_features(values):
    X, y = [], []
    for i in range(LAG, len(values)):
        X.append(values[i - LAG:i])
        y.append(values[i])
    return np.array(X), np.array(y)


def train_and_select(prices):
    if len(prices) < LAG + 10:
        return None

    prices = prices[-ROLLING_WINDOW_DAYS:]
    values = [p.close_price for p in prices]

    X, y = _create_lag_features(values)

    split = int(len(X) * 0.8)

    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_mse = mean_squared_error(y_test, lr.predict(X_test))

    rf = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )
    rf.fit(X_train, y_train)
    rf_mse = mean_squared_error(y_test, rf.predict(X_test))

    best_model = lr if lr_mse < rf_mse else rf
    model_name = "LinearRegression" if lr_mse < rf_mse else "RandomForest"

    best_model.fit(X, y)

    return best_model, model_name, values


def predict_next(prices):
    result = train_and_select(prices)
    if not result:
        return None

    model, name, values = result
    last_window = np.array(values[-LAG:]).reshape(1, -1)
    prediction = model.predict(last_window)[0]

    return {
        "predicted_next_price": round(float(prediction), 2),
        "model_used": name,
        "lag_used": LAG,
        "data_points": len(values),
    }