# Documentation API


This document provides an overview of the Template API, including its purpose, functionality, and usage.

## Purpose

The Template API is designed to manage user data, authenticate users, and interact with a database. It provides endpoints to create and manage users, generate authentication tokens, and perform CRUD operations.

## Features

- User creation and management
- Token generation and verification
- CRUD operations for data
- Database interactions with SQLAlchemy
- Authentication with JWT

## Getting Started

1. **Setup**: Configure environment variables and dependencies.
2. **Run**: Start the FastAPI server.
3. **Use**: Make API requests to the endpoints defined in the documentation.

Refer to the [API Documentation](main.md) for detailed information on each endpoint and its usage.



## Code Structure

The Template API project is organized into several key files and directories, each serving a specific purpose in the application. Here’s a high-level overview of the project structure:

- **main.py**: The entry point of the API application. It initializes the FastAPI application, sets up routing, and may include logic for starting the server. This file typically includes the creation of the FastAPI app instance and the inclusion of router modules.

- **database.py**: Contains the database configuration and setup, including SQLAlchemy engine, session management, and database models.

- **models.py**: Defines the SQLAlchemy models used in the application, including the User model and any other entities.

- **crud.py**: Implements the CRUD (Create, Read, Update, Delete) operations for interacting with the database.

- **auth.py**: Handles authentication-related functionality, including token creation, password hashing, and verification.

- **schemas.py**: Defines the Pydantic models (schemas) used for request and response validation.

- **.env**: Environment configuration file where sensitive data and configuration parameters such as database credentials and secret keys are stored.

- **router/**
  - **user_router.py**: Contains the routes and logic related to user management, including endpoints for user creation and token generation.
  - **data_router.py**: Contains the routes and logic for managing data entities.



## Environment Variable Structure

The environment variables are used to configure various aspects of the Template API application. These variables are typically stored in a `.env` file and are loaded into the application to set up database connections, authentication, and other configurations. Below is the structure of the `.env` file along with explanations for each variable:

```python
    # Determines whether to use PostgreSQL or SQLite as the database.
    # 1 for PostgreSQL, 0 for SQLite
    IS_POSTGRES=0

    # PostgreSQL Configuration (used if IS_POSTGRES is set to 1)
    DB_USERNAME=""           # The username for the PostgreSQL database
    DB_HOSTNAME=""           # The hostname or IP address of the PostgreSQL server
    DB_PORT=""               # The port number on which the PostgreSQL server is listening
    DB_NAME=""               # The name of the PostgreSQL database
    DB_PASSWORD=""           # The password for the PostgreSQL user

    # Secret key used for encoding and decoding JWT tokens
    SECRET_KEY="your_secret_key"

    # Algorithm used for encoding JWT tokens
    ALGORITHM="HS256"       # The algorithm used to sign JWT tokens. HS256 is a common choice.

    # Access token expiration time in minutes
    ACCESS_TOKEN_EXPIRE_MINUTES=30
```