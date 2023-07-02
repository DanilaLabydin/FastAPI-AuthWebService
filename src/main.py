from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

import crud, models, schemas
from database import SessionLocal, engine
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "hashed_password": "secretfakehash",
#         "salary": 5000,
#         "promotion_date": "01-01-2023",
#         "is_active": True,
#     },
#     "user3": {
#         "username": "user3",
#         "hashed_password": "testfakehash",
#         "salary": 1000,
#         "promotion_date": "12-12-2023",
#         "is_active": True,
#     }
# }


models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
    

def read_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserInDB(username=db_user.username,
                    hashed_password=db_user.hashed_password,
                    salary=db_user.salary,
                    promotion_date=db_user.promotion_date,
                    is_active=db_user.is_active
                    )

    
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


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    if plain_password + 'fakehash' == hashed_password:
        return True
    
    return False


def get_password_hash(password):
    return password + 'fakehash'


def authenticate_user(db, username: str, password: str):
    user = read_user(username, db)
    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    user = read_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


# @app.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {'token': token}


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


@app.post("/register/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already exists")
    user.password = get_password_hash(user.password)
    return crud.create_user(db, user=user)


# @app.post("/users/{user_id}/tokens/", response_model=schemas.Token)
# def create_token_for_user(user_id: int, token: schemas.TokenCreate, db: Session = Depends(get_db)):
#     return crud.create_user_token(db=db, token=token, user_id=user_id)


# @app.get("/tokens/", response_model=list[schemas.Token])
# def read_tokens(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_tokens(db, skip=skip, limit=limit)
#     return items
