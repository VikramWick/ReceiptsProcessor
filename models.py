from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    vendor = Column(String, index=True)
    date = Column(DateTime)
    total = Column(Float)
    raw_text = Column(String)