from datetime import datetime, timedelta, timezone
from typing import Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from crud import get_user

import os 
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def has_access(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),db: Session = Depends(get_db)):
    """
    Validates the access token provided in the request headers.

    Args:
        credentials (HTTPAuthorizationCredentials): The bearer token credentials.

    Returns:
        bool: True if the user has access, otherwise raises HTTPException.

    Raises:
        HTTPException: If the token is invalid or the user is not authorized.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
    except JWTError:
        raise credentials_exception
    if get_user(db, username):
        return True
    else:
        raise credentials_exception

def create_access_token(data: dict):
    """
    Create a JSON Web Token (JWT) with an expiration time.

    Args:
        data (dict): The payload data to encode in the JWT. This should be a dictionary containing the claims to be included in the token.

    Returns:
        str: The encoded JWT as a string.

    Notes:
        The token will include an 'exp' claim indicating the expiration time, which is set to the current time plus the number of minutes specified by `ACCESS_TOKEN_EXPIRE_MINUTES`.
    """
    to_encode = data.copy()
    print(to_encode)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    """
    Verify if the provided plain password matches the hashed password.

    Args:
        plain_password (str): The plain text password to check.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Generate a hashed version of the provided password.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)