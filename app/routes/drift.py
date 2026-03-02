from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.stock import Prediction
from app.core.config import DRIFT_THRESHOLD_PERCENT

router = APIRouter(tags=["Model Monitoring"])


@router.get("/drift-status/{stock_id}")
def drift_status(stock_id: int, db: Session = Depends(get_db)):
    """
    Detect model drift based on latest evaluated prediction.
    """

    latest = (
        db.query(Prediction)
        .filter(Prediction.stock_id == stock_id)
        .filter(Prediction.error_percentage.isnot(None))
        .order_by(Prediction.timestamp.desc())
        .first()
    )

    if not latest:
        return {"message": "No evaluated predictions yet"}

    drift_detected = latest.error_percentage > DRIFT_THRESHOLD_PERCENT

    return {
        "latest_error_percentage": latest.error_percentage,
        "drift_detected": drift_detected,
        "threshold": DRIFT_THRESHOLD_PERCENT,
    }