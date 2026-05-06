from datetime import datetime

from pydantic import BaseModel


class Status(BaseModel):
    id: int
    device_id: int
    address: int
    status: str
    timestamp: datetime

    class Config:
        from_attributes = True
