from fastapi import FastAPI, Depends
from fastapi.params import Depends
from models import Base
from database import engine
import router.user_router as user_router, auth, router.data_router as data_router

app = FastAPI()

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Define a list of dependencies for protected routes
PROTECTED = [Depends(auth.has_access)]

# Include the user router with the "/user" prefix
app.include_router(
    user_router.router,
    prefix="/user",
)

# Include the data router with the "/data" prefix and apply protection dependencies
app.include_router(
    data_router.router,
    prefix="/data",
    dependencies=PROTECTED
)