from sqlalchemy import Column, Integer, Float, Date
from database import Base

class CropPrice(Base):
    """Daily cereal price snapshot from the official source table."""
    __tablename__ = "crop_prices"

    # Weekly publication date used as the natural primary key.
    date = Column(Date, nullable=False, unique=True, primary_key=True)
    feed_wheat = Column(Float, default=0)
    barley = Column(Float, default=0)
    triticale = Column(Float, default=0)
    rye = Column(Float, default=0)
    oats = Column(Float, default=0)
    corn = Column(Float, default=0)