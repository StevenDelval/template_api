import os
import sys
import importlib
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


@pytest.mark.parametrize("is_postgres, expected_database", [
    ("1", "testdb"),
    ("0", "database.db")
])
def test_database_name(is_postgres,expected_database,mock_env_variables):
    """
    Test the database URL is correctly set for SQLite.
    """
    with patch.dict(os.environ, {
        "IS_POSTGRES": is_postgres
    }):
        database_module_name = 'api.database'  
        if database_module_name in sys.modules:
            importlib.reload(sys.modules[database_module_name])
        from ..database import engine
        assert engine.url.database == expected_database



@pytest.mark.parametrize("is_postgres", [
    ("1"),
    ("0")
])
def test_engine_creation(is_postgres,mock_env_variables):
    """
    Test the creation of the SQLAlchemy engine for SQLite.
    """
    with patch.dict(os.environ, {
        "IS_POSTGRES": is_postgres
    }):
        database_module_name = 'api.database'  
        if database_module_name in sys.modules:
            importlib.reload(sys.modules[database_module_name])
        from ..database import engine
        assert isinstance(engine, Engine)  # Check if engine is an instance of Engine



@pytest.mark.parametrize("is_postgres, expected_url", [
    ("1", "postgresql://user:***@localhost:5432/testdb"),
    ("0", "sqlite:///database.db")
])
def test_database_url(is_postgres, expected_url,mock_env_variables):
    """
    Test the database URL is correctly set for postgres.
    """
    with patch.dict(os.environ, {
        "IS_POSTGRES": is_postgres
    }):
        database_module_name = 'api.database'  
        if database_module_name in sys.modules:
            importlib.reload(sys.modules[database_module_name])
        from api.database import engine
        assert str(engine.url) == expected_url




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
