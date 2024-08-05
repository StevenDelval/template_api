from fastapi import FastAPI, Depends
from fastapi.params import Depends
from models import Base
from database import engine
import router.user_router as user_router, auth, router.data_router as data_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

# routes
PROTECTED = [Depends(auth.has_access)]

app.include_router(
    user_router.router,
    prefix="/user",
)

app.include_router(
    data_router.router,
    prefix="/data",
    dependencies=PROTECTED
)