from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from . database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, unique=True, index=True)
    salary = Column(Integer, unique=False, index=False)
    promotion_date = Column(DateTime)
    is_active = Column(Boolean, default=True)

