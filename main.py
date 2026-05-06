from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from database.database import SessionLocal, init_db, Base
from routes.Item import router as item_router
from routes.status import router as status_router
from services.modbus_service import modbus_client
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=== Tables registered:", Base.metadata.tables.keys())
    await init_db()
    print("=== DB initialized")
    yield
    await modbus_client.disconnect()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


app.include_router(status_router, prefix="/api", tags=["status"])
app.include_router(item_router, prefix="/api", tags=["item"])

