from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """
    Schema for user registration request.

    Attributes:
        email: Valid email address for the new user.
        password: Plain text password (will be hashed before storage).
    """

    email: EmailStr = Field(examples=["user@example.com"])
    password: str = Field(min_length=8, max_length=100, examples=["securepassword123"])


class UserResponse(BaseModel):
    """
    Schema for user data returned by the API.

    Never includes the password or hashed_password for security reasons.

    Attributes:
        id: Unique identifier of the user.
        email: User's email address.
        created_at: Timestamp when the user was created.
    """

    id: int
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    """
    Schema for user login request.

    Attributes:
        email: Registered email address.
        password: Plain text password to verify.
    """

    email: EmailStr
    password: str
