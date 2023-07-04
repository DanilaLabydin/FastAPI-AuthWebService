from sqlalchemy.orm import Session

from . models import User


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db, user):
    db_user = User(username=user.get('username'), hashed_password=user.get('password'), promotion_date=user.get('promotion_date'), salary=user.get('salary'), is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
