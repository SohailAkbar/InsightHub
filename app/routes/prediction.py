from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.stock import StockPriceHistory, Prediction
from app.services.prediction_service import predict_next

router = APIRouter(tags=["Prediction"])


@router.get("/predict/{stock_id}")
def predict(stock_id: int, db: Session = Depends(get_db)):
    """
    Generate next price prediction and store it.
    """

    prices = (
        db.query(StockPriceHistory)
        .filter(StockPriceHistory.stock_id == stock_id)
        .order_by(StockPriceHistory.timestamp.asc())
        .all()
    )

    if not prices:
        raise HTTPException(status_code=404, detail="No price data found")

    result = predict_next(prices)

    if not result:
        raise HTTPException(status_code=400, detail="Not enough data")

    new_prediction = Prediction(
        stock_id=stock_id,
        predicted_price=result["predicted_next_price"],
        timestamp=datetime.utcnow(),
    )

    db.add(new_prediction)
    db.commit()

    return result