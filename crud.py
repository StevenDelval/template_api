from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, username: str):
    """
    Retrieve a user from the database by their username.

    Args:
        db (Session): The SQLAlchemy database session used to query the database.
        username (str): The username of the user to retrieve.

    Returns:
        User: The user object if found, otherwise None.
        
    Notes:
        The function performs a query to find a user with the matching username. 
        It returns the first matching user or None if no user is found.
    """
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.

    Args:
        db (Session): The SQLAlchemy database session used to interact with the database.
        user (UserCreate): The user data to create, including username and password.

    Returns:
        User: The created user object with an assigned ID.
        
    Notes:
        The function hashes the provided password using `pwd_context.hash` and creates a new `User` 
        instance with the hashed password. The new user is then added to the database, committed, 
        and refreshed to obtain the new user’s ID.
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user