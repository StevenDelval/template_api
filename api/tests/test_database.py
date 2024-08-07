import os
import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
  # Adjust according to your project structure

@pytest.fixture
def mock_env_variables():
    """
    Fixture to mock environment variables for testing.
    """
    with patch.dict(os.environ, {
        "IS_POSTGRES": "0",
        "DB_USERNAME": "user",
        "DB_HOSTNAME": "localhost",
        "DB_PORT": "5432",
        "DB_NAME": "testdb",
        "DB_PASSWORD": "password"
    }):
        yield


def test_database_url_sqlite(mock_env_variables):
    """
    Test the database URL is correctly set for SQLite.
    """
    from ..database import engine
    assert engine.url.database == "database.db"

def test_engine_creation_sqlite(mock_env_variables):
    """
    Test the creation of the SQLAlchemy engine for SQLite.
    """
    from ..database import engine
    assert isinstance(engine, Engine)  # Check if engine is an instance of Engine

def test_database_url_postgres(mock_env_variables):
    """
    Test the database URL is correctly set for postgres.
    """
    with patch.dict(os.environ, {
        "IS_POSTGRES": "1"
    }):
        from ..database import engine
        assert engine.url.database == "testdb"

def test_engine_creation_postgres(mock_env_variables):
    """
    Test the creation of the SQLAlchemy engine for postgres.
    """
    with patch.dict(os.environ, {
        "IS_POSTGRES": "1"
    }):
        from ..database import engine
        assert isinstance(engine, Engine)  # Check if engine is an instance of Engine


def test_session_creation(mock_env_variables):
    """
    Test that the session factory creates a valid session.
    """
    from ..database import Session
    session = Session()
    assert session is not None
    session.close()

def test_get_db_function(mock_env_variables):
    """
    Test the get_db function to ensure it yields a session and cleans up properly.
    """
    from ..database import get_db
    db_gen = get_db()
    db = next(db_gen)
    assert db is not None
    db.close()
    with pytest.raises(StopIteration):
        next(db_gen)
