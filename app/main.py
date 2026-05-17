from fastapi import FastAPI
from app.database import Base, engine

from app.database import Base, engine
from app.models.user import User
from app.models.email import Email
from app.models.draft import Draft

from app.routes.auth_routes import router as auth_router
from app.routes.gmail_routes import router as gmail_router
from app.routes.draft_routes import router as draft_router

app = FastAPI()

Base.metadata.create_all(bind=engine)



app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(gmail_router, prefix="/gmail", tags=["Gmail"])
app.include_router(draft_router, prefix="/draft", tags=["Draft"])

@app.get("/")
def home():
    return {"message": "Draftly Running"}
