from sqlalchemy import Boolean, Column, Integer, String, DateTime


from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, unique=False, index=True)
    salary = Column(Integer, unique=False, index=False)
    promotion_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
