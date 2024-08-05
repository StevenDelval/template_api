from pydantic import BaseModel

class UserCreate(BaseModel):
    """
    Pydantic model for creating a new user.

    This model is used for validating and serializing the data required to create a new user.

    Attributes:
        username (str): The username for the new user. This should be a unique identifier.
        password (str): The password for the new user. It will be hashed before storing.
    """
    username: str
    password: str

class UserOut(BaseModel):
    """
    Pydantic model for representing a user in responses.

    This model is used for serializing user data that is returned in API responses.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.

    Config:
        from_attributes (bool): This configuration allows the model to be created from ORM models directly.

    Notes:
        The `Config` subclass enables compatibility with ORM models by allowing `UserOut` to be constructed 
        from attributes of ORM models.
    """
    id: int
    username: str

    class Config:
        from_attributes = True