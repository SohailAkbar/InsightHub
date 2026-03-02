from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.stock import Prediction
import statistics

router = APIRouter(tags=["Model Metrics"])

@router.get("/model-accuracy/{stock_id}")
def model_accuracy(stock_id: int, db: Session = Depends(get_db)):
    records = db.query(Prediction)\
        .filter(Prediction.stock_id == stock_id)\
        .filter(Prediction.actual_price != None)\
        .all()

    if not records:
        return {"message": "No evaluated predictions yet"}

    errors = [
        abs(p.actual_price - p.predicted_price) / p.actual_price * 100
        for p in records
    ]

    return {
        "mean_absolute_percentage_error": round(statistics.mean(errors), 2),
        "evaluated_predictions": len(records)
    }
