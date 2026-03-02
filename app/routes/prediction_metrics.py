from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import statistics

from app.database import get_db
from app.models.stock import Prediction

router = APIRouter(tags=["Prediction Metrics"])


@router.get("/prediction-accuracy/{stock_id}")
def prediction_accuracy(stock_id: int, db: Session = Depends(get_db)):
    """
    Calculate average prediction error percentage.
    """

    records = (
        db.query(Prediction)
        .filter(Prediction.stock_id == stock_id)
        .filter(Prediction.error_percentage.isnot(None))
        .all()
    )

    if not records:
        return {"message": "No evaluated predictions yet"}

    errors = [r.error_percentage for r in records]

    return {
        "mean_error_percentage": round(statistics.mean(errors), 4),
        "evaluated_predictions": len(errors),
    }