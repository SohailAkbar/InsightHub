from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.stock import Stock
from app.schemas.stock import StockCreate, StockResponse

router = APIRouter(prefix="/stocks", tags=["Stocks"])


@router.post("", response_model=StockResponse)
def create_stock(stock: StockCreate, db: Session = Depends(get_db)):
    """
    Create a new stock entry.
    Prevents duplicate symbols.
    """
    existing = db.query(Stock).filter(Stock.symbol == stock.symbol).first()
    if existing:
        raise HTTPException(status_code=400, detail="Stock already exists")

    new_stock = Stock(symbol=stock.symbol, name=stock.name)
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)

    return new_stock


@router.get("", response_model=list[StockResponse])
def get_stocks(db: Session = Depends(get_db)):
    """
    Retrieve all registered stocks.
    """
    return db.query(Stock).all()