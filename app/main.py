from fastapi import FastAPI
from app.database import engine, Base
import app.models.stock

from app.routes.health import router as health_router
from app.routes.stocks import router as stocks_router
from app.routes.prices import router as prices_router
from app.routes.analytics import router as analytics_router
from app.routes.prediction import router as prediction_router
from app.routes.model_compare import router as model_compare_router
from app.routes.prediction_metrics import router as prediction_metrics_router  # ← add this
from app.routes.retrain import router as retrain_router
from app.routes.drift import router as drift_router
from app.routes.model_info import router as model_info_router

app = FastAPI(title="InsightHub API")

Base.metadata.create_all(bind=engine)

app.include_router(health_router)
app.include_router(stocks_router)
app.include_router(prices_router)
app.include_router(analytics_router)
app.include_router(prediction_router)
app.include_router(model_compare_router)
app.include_router(retrain_router)
app.include_router(drift_router)
app.include_router(model_info_router)
app.include_router(prediction_metrics_router)  # ← add this
