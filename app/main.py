from fastapi import FastAPI
from app.utils.logger import logger
from app.database import Base, engine
from app.models.user import User
from app.models.email import Email
from app.models.draft import Draft
from fastapi import Request
from fastapi.responses import JSONResponse
from app.routes.auth_routes import router as auth_router
from app.routes.gmail_routes import router as gmail_router
from app.routes.draft_routes import router as draft_router
from app.core.exceptions import (
    GmailTokenRefreshException
)
from app.routes.dashboard_routes import router as dashboard_router
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(gmail_router, prefix="/gmail", tags=["Gmail"])
app.include_router(draft_router, prefix="/draft", tags=["Draft"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])

@app.get("/")
def home():
    return {"message": "Draftly Running"}

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY")
)

@app.exception_handler(
    GmailTokenRefreshException
)
async def gmail_exception_handler(
    request: Request,
    exc: GmailTokenRefreshException
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": str(exc)
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.error(str(exc))

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error"
        }
    )