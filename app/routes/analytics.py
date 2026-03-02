from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.stock import StockPriceHistory
from app.services.analytics_service import calculate_analytics

router = APIRouter(tags=["Analytics"])

@router.get("/analytics/{stock_id}")
def analytics(stock_id: int, db: Session = Depends(get_db)):
    """
    Compute descriptive analytics for stock.
    """

    prices = (
        db.query(StockPriceHistory)
        .filter(StockPriceHistory.stock_id == stock_id)
        .order_by(StockPriceHistory.timestamp.asc())
        .all()
    )

    result = calculate_analytics(prices)

    if not result:
        raise HTTPException(status_code=404, detail="No data found")

    return result