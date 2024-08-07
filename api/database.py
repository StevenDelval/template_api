from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker, declarative_base

import os 
from dotenv import load_dotenv
load_dotenv()

# Determine the database URL based on environment variables
if bool(int(os.getenv("IS_POSTGRES"))):
    username = os.getenv("DB_USERNAME")
    hostname = os.getenv("DB_HOSTNAME")
    port = os.getenv("DB_PORT")
    database_name = os.getenv("DB_NAME")
    password = os.getenv("DB_PASSWORD")
    bdd_path = f"postgresql://{username}:{password}@{hostname}:{port}/{database_name}"
else:
    bdd_path = 'sqlite:///database.db'

# Create a SQLAlchemy engine for the specified database
engine = create_engine(bdd_path, connect_args={"check_same_thread": False})

# Create a session factory bound to the engine
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base class for declarative class definitions
Base: DeclarativeMeta = declarative_base()


def get_db():
    """
    Dependency that provides a SQLAlchemy database session.

    Yields:
        Session: A SQLAlchemy session instance that is used to interact with the database.

    Notes:
        The session is created and yielded for use in database operations. After the operation, 
        the session is closed to release the database connection.
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()