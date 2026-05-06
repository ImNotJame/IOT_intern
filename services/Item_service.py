from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession



from models.Item_model import ItemDB_model
from repositories.item_repository import ItemRepository

from schemas.test_schemas import ItemCreate


async def create_item_service(item: ItemCreate, db:AsyncSession):
    db_item = ItemDB_model(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def get_items_service(db:AsyncSession):
    item_repo = ItemRepository(db)
    result = await item_repo.find_all()
    return result




async def get_item_service(item_id:int, db:AsyncSession):
    item_repo = ItemRepository(db)
    db_item =  await item_repo.find_by_id(item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


async def update_item_service(item_id:int, item: ItemCreate, db:AsyncSession):
    item_repo = ItemRepository(db)

    db_item = await item_repo.find_by_id(item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def delete_item_service(item_id:int, db:AsyncSession):
    item_repo = ItemRepository(db)

    db_item = await item_repo.find_by_id(item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(db_item)
    await db.commit()
    return {"message": "Item deleted"}

