from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    salary: int | None = None
    promotion_date: str | None = None


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class User(UserBase):
    is_active: bool | None = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserInDB(User):
    hashed_password: str