from sqlalchemy import Column, Integer, ForeignKey, String, Float, Text

from database.database import Base


class ItemDB_model(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    tax = Column(Float, nullable=True)

