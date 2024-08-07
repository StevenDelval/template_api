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
def test_database_name(is_postgres, expected_database, mock_env_variables):
    """
    Test if the database URL is correctly set based on the environment variable.

    This function mocks the environment variable `IS_POSTGRES` to simulate
    different database configurations. It reloads the `api.database` module
    to ensure that any changes in the configuration are picked up, and then
    verifies that the database URL's database name matches the expected value.

    Args:
        is_postgres (bool): If True, simulate a PostgreSQL environment; otherwise, simulate SQLite.
        expected_database (str): The expected database name in the URL.
        mock_env_variables (dict): A dictionary of environment variables to mock (not used in the function).

    Raises:
        AssertionError: If the actual database name does not match `expected_database`.
    """
    with patch.dict(os.environ, {
        "IS_POSTGRES": str(is_postgres).lower()
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
def test_engine_creation(is_postgres, mock_env_variables):
    """
    Test the creation of the SQLAlchemy engine based on the environment variable.

    This function mocks the environment variable `IS_POSTGRES` to simulate
    different database configurations. It reloads the `api.database` module
    to ensure that the latest configuration is used and verifies that the
    created SQLAlchemy engine is an instance of `Engine`.

    Args:
        is_postgres (bool): If True, simulate a PostgreSQL environment; otherwise, simulate SQLite.
        mock_env_variables (dict): A dictionary of environment variables to mock (not used in the function).

    Raises:
        AssertionError: If the created engine is not an instance of `Engine`.
    """
    with patch.dict(os.environ, {
        "IS_POSTGRES": str(is_postgres).lower()
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
def test_database_url(is_postgres, expected_url, mock_env_variables):
    """
    Test if the database URL is correctly set based on the environment variable.

    This function mocks the environment variable `IS_POSTGRES` to simulate
    different database configurations (e.g., PostgreSQL or SQLite). It reloads
    the `api.database` module to ensure that any changes in configuration are
    applied, and then verifies that the database URL matches the expected value.

    Args:
        is_postgres (bool): If True, simulate a PostgreSQL environment; otherwise, simulate SQLite.
        expected_url (str): The expected database URL.
        mock_env_variables (dict): A dictionary of environment variables to mock (not used in this function).

    Raises:
        AssertionError: If the actual database URL does not match `expected_url`.
    """
    with patch.dict(os.environ, {
        "IS_POSTGRES": str(is_postgres).lower()
    }):
        database_module_name = 'api.database'
        if database_module_name in sys.modules:
            importlib.reload(sys.modules[database_module_name])
        from api.database import engine
        assert str(engine.url) == expected_url  # Check if the actual database URL matches the expected URL



def test_session_creation(mock_env_variables):
    """
    Test that the session factory creates a valid SQLAlchemy session.

    This function imports the `Session` factory from the `database` module and
    verifies that it can create a session instance. The test ensures that the
    session is not `None` and then closes it to ensure proper resource cleanup.

    Args:
        mock_env_variables (dict): A dictionary of environment variables to mock (not used in this function).

    Raises:
        AssertionError: If the session is `None` or if there are any issues creating the session.
    """
    from ..database import Session  # Import Session from the database module

    # Create a session using the session factory
    session = Session()
    
    # Check if the session is created and is not None
    assert session is not None, "Session creation failed: Session is None."
    
    # Close the session to clean up resources
    session.close()


def test_get_db_function(mock_env_variables):
    """
    Test the `get_db` function to ensure it yields a session and cleans up properly.

    This function tests the `get_db` generator function to ensure that it:
    1. Yields a valid session object.
    2. Properly raises `StopIteration` after the session is closed, indicating that no more sessions are available.

    Args:
        mock_env_variables (dict): A dictionary of environment variables to mock (not used in this function).

    Raises:
        AssertionError: If the session is `None` or if `StopIteration` is not raised after the session is closed.
    """
    from ..database import get_db
    
    db_gen = get_db()
    
    # Fetch the session from the generator
    db = next(db_gen)
    
    # Ensure the session is not None
    assert db is not None, "The database session is None."

    # Close the session to ensure proper cleanup
    db.close()
    
    # Ensure that no more sessions are available after closing the session
    with pytest.raises(StopIteration):
        next(db_gen)
