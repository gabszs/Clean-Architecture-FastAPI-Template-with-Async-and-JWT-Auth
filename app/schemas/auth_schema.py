from datetime import datetime

from pydantic import BaseModel
from pydantic import EmailStr

from app.schemas.user_schema import User


class SignIn(BaseModel):
    email: EmailStr
    password: str


class SignUp(BaseModel):
    email: EmailStr
    password: str
    username: str


class Payload(BaseModel):
    id: str
    email: EmailStr
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


class SignInResponse(BaseModel):
    access_token: str
    expiration: datetime
    user_info: User
