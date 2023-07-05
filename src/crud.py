from sqlalchemy.orm import Session
import logging


from .models import User


LOGGER = logging.getLogger(__name__)


def get_user_by_username(db: Session, username: str):
    try:
        user = db.query(User).filter(User.username == username).first()
        return user
    except Exception as e:
        LOGGER.error(f"Could not fetch user from DB: {e}")
        return None


def create_user(db, user):
    try:
        db_user = User(
            username=user.username,
            hashed_password=user.password,
            promotion_date=user.promotion_date,
            salary=user.salary,
            is_active=True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        LOGGER.error(f"Could not create user: {e}")
        return None
