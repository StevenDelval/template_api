# Template API

Welcome to the Template API project. This API is designed to manage user data, handle authentication, and interact with a database. It is built using FastAPI and SQLAlchemy, and supports JWT-based authentication.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)

## Features

- User management (create and authenticate users)
- Token-based authentication using JWT
- Database interactions with SQLAlchemy
- Supports PostgreSQL and SQLite

## Installation

To get started with the Template API, follow these steps:

1. **Clone the repository:**

    ```sh
    git clone https://github.com/StevenDelval/template_api.git
    cd template_api
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

Create a .env file in the root directory and add the following configuration:

    ```ini

    IS_POSTGRES=0
    DB_USERNAME=""
    DB_HOSTNAME=""
    DB_PORT=""
    DB_NAME=""
    DB_PASSWORD=""
    SECRET_KEY="your_secret_key"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5. **Run database migrations:**

If using PostgreSQL, ensure your database is set up and accessible. For SQLite, no additional setup is needed.

6. **Start the FastAPI server:**

    ```sh
    uvicorn main:app --reload
    ```

## Configuration

- Database: Configure the database type and credentials in the .env file. Set IS_POSTGRES to 1 for PostgreSQL or 0 for SQLite.
- Authentication: Set SECRET_KEY, ALGORITHM, and ACCESS_TOKEN_EXPIRE_MINUTES in the .env file to configure JWT settings.

## Usage

Once the server is running, you can access the API at http://127.0.0.1:8000. The FastAPI documentation is available at http://127.0.0.1:8000/docs.

## API Documentation

For detailed API documentation, refer to the [Documentation section](https://stevendelval.github.io/template_api/). 
It includes information on the endpoints, request and response formats, and examples.