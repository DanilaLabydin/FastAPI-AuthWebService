from datetime import datetime, timedelta
from typing import Annotated
import logging

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext


from .crud import get_user_by_username, create_user
from .models import Base
from .database import SessionLocal, engine
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from .schemas import UserCreate, User, Token, TokenData, UserInDB


LOGGER = logging.getLogger(__name__)
Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def read_user(username: str, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        user = UserInDB(
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            salary=db_user.salary,
            promotion_date=str(db_user.promotion_date),
            is_active=db_user.is_active,
        )
        return user
    except Exception as e:
        LOGGER.error(f"Error reading user: {e}")
        return None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    if plain_password + "fakehash" == hashed_password:
        return True

    return False


def get_password_hash(password):
    return password + "fakehash"


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


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
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
    user = read_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return {
        "username": current_user.username,
        "salary": current_user.salary,
        "promotion_date": current_user.promotion_date,
    }


@app.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already exists")
    user.password = get_password_hash(user.password)
    new_user = create_user(db, user=user)
    if new_user is None:
        raise HTTPException(status_code=500, detail="db could not create the user")

    return {"id": new_user.id, "username": new_user.username}
