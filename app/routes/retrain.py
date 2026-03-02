from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.stock import StockPriceHistory
from app.services.prediction_service import predict_next

router = APIRouter(tags=["Model Management"])


@router.post("/retrain/{stock_id}")
def retrain_model(stock_id: int, db: Session = Depends(get_db)):
    """
    Retrain model using latest rolling window data.
    """

    prices = (
        db.query(StockPriceHistory)
        .filter(StockPriceHistory.stock_id == stock_id)
        .order_by(StockPriceHistory.timestamp.asc())
        .all()
    )

    if len(prices) < 10:
        raise HTTPException(
            status_code=400,
            detail="Not enough data to retrain",
        )

    result = predict_next(prices)

    return {
        "message": "Model retrained successfully",
        "data_points_used": len(prices),
        "timestamp": datetime.utcnow(),
        "model_preview_prediction": result["predicted_next_price"],
    }