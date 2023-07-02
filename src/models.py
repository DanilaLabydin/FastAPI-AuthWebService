from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, unique=True, index=True)
    salary = Column(Integer, unique=False, index=False)
    promotion_date = Column(DateTime)
    is_active = Column(Boolean, default=True)

    token = relationship("Token", back_populates="user")


class Token(Base):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True)
    expires = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="token")
