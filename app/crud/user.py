from typing import Optional

from sqlalchemy.orm import Session

from app import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str, user_id: Optional[int] = None):
    db_users = db.query(models.User).filter(models.User.email == email)
    if user_id:
        db_users = db_users.filter(models.User.id != user_id)

    return db_users.first()


def get_user_by_code_and_phone(
    db: Session, country_code: int, phone_number: int, user_id: Optional[int] = None
):
    db_users = db.query(models.User).filter(
        models.User.country_code == country_code,
        models.User.phone_number == phone_number,
    )

    if user_id:
        db_users = db_users.filter(models.User.id != user_id)

    return db_users.first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_in: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    for var, value in vars(user_in).items():
        setattr(db_user, var, value) if value else None

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
