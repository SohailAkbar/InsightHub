from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.stock import Prediction
import statistics

router = APIRouter(tags=["Model Insights"])


@router.get("/model-info/{stock_id}")
def model_info(stock_id: int, db: Session = Depends(get_db)):

    predictions = (
        db.query(Prediction)
        .filter(Prediction.stock_id == stock_id)
        .all()
    )

    if not predictions:
        return {"message": "No model activity yet"}

    errors = [p.error_percentage for p in predictions if p.error_percentage]

    return {
        "total_predictions": len(predictions),
        "evaluated_predictions": len(errors),
        "average_error_percentage": round(statistics.mean(errors), 4) if errors else None
    }
