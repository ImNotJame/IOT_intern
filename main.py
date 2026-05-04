from fastapi import FastAPI
from pymodbus.client import ModbusTcpClient
from fastapi.middleware.cors import CORSMiddleware
from database.database import SessionLocal, init_db, Base
from routes.Item import router as item_router
from contextlib import asynccontextmanager

import models.Item_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=== Tables registered:", Base.metadata.tables.keys())
    await init_db()
    print("=== DB initialized")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def get_data(number: int):
    return {"your num is": number}

device_status = "off"
@app.post("/{status}")
def trigger(status: str):
    global device_status
    #client = ModbusTcpClient(host="172.20.9.111", port=502)
    #client.connect()
    if status == "on":
        device_status = "on"
        #client.write_coil(0,True)
        pass
    else:
        device_status = "off"
       #client.write_coil(0,False)
        pass
    #client.close()
    return {"status": status}


@app.get("/status")
def get_status():
    print(device_status)
    return {"status": device_status}


app.include_router(item_router, prefix="/api", tags=["item"])


