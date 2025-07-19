
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc
from typing import List, Optional
from datetime import date
import statistics

from . import models, schemas, ocr_processor
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["http://localhost:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.delete("/receipts/{receipt_id}", status_code=200)
def delete_receipt(receipt_id: int, db: Session = Depends(get_db)):
    """Deletes a receipt from the database by its ID."""
    db_receipt = db.query(models.Receipt).filter(models.Receipt.id == receipt_id).first()
    if db_receipt is None:
        raise HTTPException(status_code=404, detail="Receipt not found")
    
    db.delete(db_receipt)
    db.commit()
    return {"detail": "Receipt deleted successfully"}

@app.post("/upload/", response_model=schemas.Receipt)
async def upload_receipt(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Handles uploading image, pdf, or txt files for processing."""
    content_type = file.content_type
    raw_text = ""
    
    if content_type.startswith("image/"):
        raw_text = ocr_processor.extract_text_from_image(file.file)
    elif content_type == "application/pdf":
        raw_text = ocr_processor.extract_text_from_pdf(file.file)
    elif content_type == "text/plain":
        raw_text = ocr_processor.extract_text_from_txt(file.file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    parsed_data = ocr_processor.parse_receipt_data(raw_text)

    db_receipt = models.Receipt(
        raw_text=raw_text,
        vendor=parsed_data.get("vendor"),
        date=parsed_data.get("date"),
        total=parsed_data.get("total")
    )
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)
    return db_receipt

@app.get("/receipts/", response_model=List[schemas.Receipt])
def get_receipts(
    db: Session = Depends(get_db),
    search: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    sort_by: Optional[str] = Query('date', enum=['date', 'vendor', 'total']),
    order: Optional[str] = Query('desc', enum=['asc', 'desc'])
):
    """Retrieves receipts with filtering, searching, and sorting."""
    query = db.query(models.Receipt)
    
    if search:
        query = query.filter(models.Receipt.vendor.ilike(f"%{search}%"))
    if start_date:
        query = query.filter(models.Receipt.date >= start_date)
    if end_date:
        query = query.filter(models.Receipt.date <= end_date)

    sort_column = getattr(models.Receipt, sort_by)
    if order == 'asc':
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))
        
    return query.all()

@app.get("/receipts/stats/")
def get_receipt_stats(db: Session = Depends(get_db)):
    """Calculates full statistics: sum, mean, median, and mode."""
    totals = [r.total for r in db.query(models.Receipt).filter(models.Receipt.total != None).all()]
    if not totals:
        return {"total_spending": 0, "receipt_count": 0, "average_spending": 0, "median_spending": 0, "mode_spending": 0}

    try:
        mode = statistics.mode(totals)
    except statistics.StatisticsError:
        mode = "No unique mode"

    return {
        "total_spending": round(sum(totals), 2),
        "receipt_count": len(totals),
        "average_spending": round(statistics.mean(totals), 2),
        "median_spending": round(statistics.median(totals), 2),
        "mode_spending": mode
    }

@app.get("/receipts/stats/vendor-frequency/")
def get_vendor_frequency(db: Session = Depends(get_db)):
    """Calculates frequency of each vendor for pie/bar charts."""
    query = db.query(
        models.Receipt.vendor, 
        func.count(models.Receipt.vendor).label('count')
    ).group_by(models.Receipt.vendor).order_by(desc('count')).all()
    return [{"vendor": vendor, "count": count} for vendor, count in query if vendor]

@app.get("/receipts/stats/monthly-spend/")
def get_monthly_spend(db: Session = Depends(get_db)):
    """Calculates total spending per month for time-series chart."""
    query = db.query(
        func.strftime('%Y-%m', models.Receipt.date).label('month'),
        func.sum(models.Receipt.total).label('total')
    ).group_by('month').order_by('month').all()
    return [{"month": month, "total": total} for month, total in query if month]
