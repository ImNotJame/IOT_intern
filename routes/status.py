

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from services.status_service import trigger_service, get_status_service, get_registers_service, get_logs_service

router = APIRouter()

@router.post("/status/{status}")
async def trigger(status: str, session: AsyncSession = Depends(get_db)):
    return await trigger_service(status, session)


@router.get("/status")
async def get_status(session: AsyncSession = Depends(get_db)):
    return await get_status_service(session)

@router.get("/logs")
async def get_logs(session: AsyncSession = Depends(get_db)):
    return await get_logs_service(session)

@router.get("/registers")
async def get_registers(session: AsyncSession = Depends(get_db)):
    return await get_registers_service(session)

