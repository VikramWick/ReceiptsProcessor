from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReceiptBase(BaseModel):
    vendor: Optional[str] = None
    date: Optional[datetime] = None
    total: Optional[float] = None

class ReceiptCreate(ReceiptBase):
    raw_text: str

class Receipt(ReceiptBase):
    id: int

    class Config:
        orm_mode = True