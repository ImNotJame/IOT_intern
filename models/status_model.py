from datetime import datetime

import pytz
from sqlalchemy import Column, Integer, String, DateTime, true

from database.database import Base

bangkok_tz = pytz.timezone('Asia/Bangkok')

def get_bangkok_time():
    return datetime.now(bangkok_tz)

class StatusModel(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, nullable=False)
    status = Column(String(255), nullable=False)
    timestamp = Column(DateTime(timezone=True),default=get_bangkok_time)