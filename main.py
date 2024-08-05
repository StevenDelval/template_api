from fastapi import FastAPI, Depends
from fastapi.params import Depends
from models import Base
from database import engine
import user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

# routes
# PROTECTED = [Depends(has_access)]

app.include_router(
    user_router.router,
    prefix="/user",
)