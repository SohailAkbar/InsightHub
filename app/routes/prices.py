from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.stock import Stock, StockPriceHistory, Prediction
from app.schemas.stock import PriceCreate, PriceResponse

router = APIRouter(tags=["Prices"])


@router.post("/prices", response_model=PriceResponse)
def add_price(price: PriceCreate, db: Session = Depends(get_db)):

    stock = db.query(Stock).filter(Stock.id == price.stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    # Insert new price
    new_price = StockPriceHistory(
        stock_id=price.stock_id,
        close_price=price.close_price,
        volume=price.volume,
        timestamp=datetime.utcnow()
    )

    db.add(new_price)
    db.commit()
    db.refresh(new_price)

    # -------- AUTO EVALUATE LATEST PREDICTION --------
    latest_prediction = (
        db.query(Prediction)
        .filter(Prediction.stock_id == price.stock_id)
        .filter(Prediction.actual_price == None)
        .order_by(Prediction.timestamp.desc())
        .first()
    )

    if latest_prediction:
        latest_prediction.actual_price = price.close_price

        error = abs(price.close_price - latest_prediction.predicted_price)
        error_percent = (error / price.close_price) * 100

        latest_prediction.error_percentage = round(error_percent, 4)
        db.commit()

    return new_price


@router.get("/prices/{stock_id}", response_model=list[PriceResponse])
def get_prices(stock_id: int, db: Session = Depends(get_db)):
    return (
        db.query(StockPriceHistory)
        .filter(StockPriceHistory.stock_id == stock_id)
        .order_by(StockPriceHistory.timestamp.asc())
        .all()
    )
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.stock import Stock, StockPriceHistory, Prediction
from app.schemas.stock import PriceCreate, PriceResponse

router = APIRouter(tags=["Prices"])


@router.post("/prices", response_model=PriceResponse)
def add_price(price: PriceCreate, db: Session = Depends(get_db)):
    """
    Insert new price and automatically evaluate latest pending prediction.
    """

    stock = db.query(Stock).filter(Stock.id == price.stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    new_price = StockPriceHistory(
        stock_id=price.stock_id,
        close_price=price.close_price,
        volume=price.volume,
        timestamp=datetime.utcnow(),
    )

    db.add(new_price)
    db.commit()
    db.refresh(new_price)

    # Evaluate latest prediction if pending
    latest_prediction = (
        db.query(Prediction)
        .filter(Prediction.stock_id == price.stock_id)
        .filter(Prediction.actual_price.is_(None))
        .order_by(Prediction.timestamp.desc())
        .first()
    )

    if latest_prediction:
        latest_prediction.actual_price = price.close_price

        error = abs(price.close_price - latest_prediction.predicted_price)
        error_percent = (
            (error / price.close_price) * 100
            if price.close_price != 0 else 0
        )

        latest_prediction.error_percentage = round(error_percent, 4)
        db.commit()

    return new_price


@router.get("/prices/{stock_id}", response_model=list[PriceResponse])
def get_prices(stock_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all price history for a stock.
    """
    return (
        db.query(StockPriceHistory)
        .filter(StockPriceHistory.stock_id == stock_id)
        .order_by(StockPriceHistory.timestamp.asc())
        .all()
    )