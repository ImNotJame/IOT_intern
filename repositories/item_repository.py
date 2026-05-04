
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models.Item_model import ItemDB_model


class ItemRepository():
    def __init__(self, db:Session):
        self.db = db


    async def find_all(self):
        query = select(ItemDB_model)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def find_by_id(self, item_id:int):
        query = select(ItemDB_model).where(ItemDB_model.id==item_id)
        result = await self.db.execute(query)
        return result.scalars().first()


