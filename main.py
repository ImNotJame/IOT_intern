from fastapi import FastAPI
from pymodbus.client import ModbusTcpClient
from fastapi.middleware.cors import CORSMiddleware
from database.database import SessionLocal, init_db, Base
from routes.Item import router as item_router
from routes.status import router as status_router
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=== Tables registered:", Base.metadata.tables.keys())
    await init_db()
    print("=== DB initialized")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)


app.include_router(status_router, prefix="/api", tags=["status"])
app.include_router(item_router, prefix="/api", tags=["item"])


