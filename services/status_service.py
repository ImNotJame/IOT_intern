from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.status_repository import StatusRepository
from services.modbus_service import modbus_client




async def trigger_service(status:str, session: AsyncSession):
    status_repo = StatusRepository(session)
    current_status = await get_status_service(session)
    if status == "on":
        if current_status["status"] == "on":
            print("status already on")
            return {"status": status}
        await modbus_client.write_coil(address=0, value=True, device_id=1)
    else:
        await modbus_client.write_coil(address=0, value=False, device_id=1)
        if current_status["status"] == "off":
            print("status already off")
            return {"status": status}
    await status_repo.add_log_by_device_id(status, device_id=1, address=0)
    return {"status": status}


async def get_status_service(session: AsyncSession):
    response = await modbus_client.read_coil(address=0, device_id=1)
    return {"status": response.bits[0]}


async def get_registers_service(session: AsyncSession):
    return await modbus_client.read_registers(address=0, count=10, device_id=2)


async def get_logs_service(session: AsyncSession):
    status_repo = StatusRepository(session)
    return await status_repo.get_logs()
