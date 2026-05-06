from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.status_model import StatusModel


class StatusRepository():

    def __init__(self, db:AsyncSession):
        self.db = db



    async def get_logs(self):
        result = await self.db.execute(select(StatusModel).order_by(StatusModel.timestamp.desc()))
        return result.scalars().all()



    async def add_log_by_device_id(self, status:str ,device_id:int):
        log = StatusModel(status=status,device_id=device_id)
        self.db.add(log)
        await self.db.commit()
        await self.db.refresh(log)
        return log


    async def get_last_status_by_device_id(self, device_id: int):
        result = await self.db.execute(select(StatusModel).filter_by(device_id=device_id).order_by(StatusModel.timestamp.desc()).limit(1))
        return result.scalar()