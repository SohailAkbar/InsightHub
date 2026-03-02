from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.stock import StockPriceHistory
from app.services.model_evaluation_service import evaluate_models

router = APIRouter(tags=["Model Comparison"])


@router.get("/model-compare/{stock_id}")
def compare_models(stock_id: int, db: Session = Depends(get_db)):
    prices = (
        db.query(StockPriceHistory)
        .filter(StockPriceHistory.stock_id == stock_id)
        .order_by(StockPriceHistory.timestamp.asc())
        .all()
    )

    result = evaluate_models(prices)

    if result is None:
        raise HTTPException(status_code=400, detail="Not enough data (minimum 5 points required)")

    return result
