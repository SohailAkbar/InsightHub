from pydantic import BaseModel
from datetime import datetime


class StockCreate(BaseModel):
    symbol: str
    name: str


class StockResponse(BaseModel):
    id: int
    symbol: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class PriceCreate(BaseModel):
    stock_id: int
    close_price: float
    volume: int


class PriceResponse(BaseModel):
    id: int
    stock_id: int
    close_price: float
    volume: int
    timestamp: datetime

    class Config:
        from_attributes = True