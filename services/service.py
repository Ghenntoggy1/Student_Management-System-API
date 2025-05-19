from db import models, schemas
import bcrypt

from sqlalchemy.orm import Session

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.Email == email).first()

def add_user(db: Session, user: schemas.UserRequest):
    salt = bcrypt.gensalt()
    password_bytes = user.password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    db_user = models.User(
        Role=user.role,
        FirstName=user.first_name,
        LastName=user.last_name,
        Email=user.email,
        Password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user