from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from models import Base, User
import crud, auth, schemas



router = APIRouter()


@router.post("/hello")
def get_hello():
    """
    Simple endpoint that returns a greeting message.

    This endpoint is a basic test route that returns a static string message.

    Returns:
        str: A greeting message "Hello !".

    Notes:
        This endpoint does not perform any database operations or require any request body.
        It is primarily used for testing and ensuring that the API is accessible.
    """
    return "Hello !"

