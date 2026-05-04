from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session


from database.database import get_db
from schemas.test_schemas import ItemResponse, ItemCreate
from services.Item_service import create_item_service, update_item_service, get_items_service, delete_item_service, \
    get_item_service

router = APIRouter()

@router.post("/item",response_model=ItemResponse)
async def create_item(item: ItemCreate, db:Session = Depends(get_db)):
    return await create_item_service(item, db)


@router.get("/item",response_model=List[ItemResponse])
async def get_items(db:Session = Depends(get_db)):
    return await get_items_service(db)


@router.get("/item/{item_id}",response_model=ItemResponse)
async def get_item(item_id:int, db:Session = Depends(get_db)):
    return await get_item_service(item_id, db)


@router.put("/item/{item_id}",response_model=ItemResponse)
async def update_item(item_id:int, item: ItemCreate, db:Session = Depends(get_db)):
    return await update_item_service(item_id, item, db)

@router.delete("/item/{item_id}")
async def delete_item(item_id:int, db:Session = Depends(get_db)):
    return await delete_item_service(item_id, db)

