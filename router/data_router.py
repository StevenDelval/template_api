from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from models import Base, User
import crud, auth, schemas



router = APIRouter()


@router.post("/hello")
def get_hello():
    return "Hello !"

