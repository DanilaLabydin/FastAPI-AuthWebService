from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    salary: int | None = None
    promotion_date: str | None = None
    is_active: bool | None = None


class UserInDB(User):
    hashed_password: str