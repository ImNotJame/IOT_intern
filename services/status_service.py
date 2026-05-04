from sqlalchemy.ext.asyncio import AsyncSession



device_status = "off"

async def trigger_service(status:str, session: AsyncSession):
    global device_status
    if status == "on":
        device_status = "on"
    else:
        device_status = "off"
    return {"status": status}


async def get_status_service(session: AsyncSession):
    return {"status": device_status}
