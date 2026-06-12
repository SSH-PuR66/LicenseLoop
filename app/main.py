from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import account, billing, licenses, pages, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="LicenseLoop", version="1.0.0", lifespan=lifespan)
app.include_router(pages.router)
app.include_router(account.router)
app.include_router(licenses.router)
app.include_router(billing.router)
app.include_router(tasks.router)
