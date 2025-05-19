from fastapi import HTTPException
from starlette import status
from db import models, schemas
import bcrypt
from sqlalchemy.orm import Session
from db.schemas import Token
from auth.auth import decode_access_token
from enums.enums import JWTValidationResultsEnum


def jwt_validation_response(jwt_token: Token):
    decoded_token = decode_access_token(token=jwt_token.access_token)
    if decoded_token == JWTValidationResultsEnum.is_expired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your token has expired. Please login again."
        )
    if decoded_token == JWTValidationResultsEnum.is_invalid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your token is invalid. Please login again."
        )
    if decoded_token == JWTValidationResultsEnum.invalid_signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your token signature is invalid. Please login again."
        )
    if decoded_token == "UNKNOWN_ERROR":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unknown error occurred while validating your token. Please login again."
        )
    return decoded_token

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