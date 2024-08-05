from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from models import Base, User
import crud, auth, schemas



router = APIRouter()


@router.post("/create_access_token")
def create_access_token(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Generate a new access token for a user based on provided credentials.

    Args:
        form_data (schemas.UserCreate): The user credentials including username and password.
        db (Session, optional): The database session dependency, used to interact with the database.

    Returns:
        dict: A dictionary containing the access token and the token type.

    Raises:
        HTTPException: If the provided credentials are incorrect, a 401 Unauthorized error is raised.

    Notes:
        The function checks the provided username and password against the stored user data in the database.
        If the credentials are valid, an access token is generated using the `create_access_token` function from the `auth` module.
    """
    user = crud.get_user(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/create_user/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.

    Args:
        user (schemas.UserCreate): The user data including username and password to be created.
        db (Session, optional): The database session dependency, used to interact with the database.

    Returns:
        schemas.UserOut: The created user information, including the user ID and username.

    Raises:
        HTTPException: If the username is already registered, a 400 Bad Request error is raised.
        
    Notes:
        The function checks if the username is already taken. If not, a new user is created using the `create_user` function from the `crud` module.
    """
    db_user = crud.get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)