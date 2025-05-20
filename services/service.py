from fastapi import HTTPException, Depends
from starlette import status
import bcrypt
from sqlalchemy.orm import Session

from models.user_model import UserModel
from models.group_model import GroupModel
from models.session_model import SessionModel
from models.course_model import CourseModel
from models.attendance_model import AttendanceModel
from models.course_group_model import CourseGroupModel
from models.student_group_model import StudentGroupModel
from schemas.schemas import Token, UserRequest, UserResponse
from auth.auth import decode_access_token, oauth2_scheme
from enums.server_enums import JWTValidationResultsEnum


def jwt_validation_response(jwt_token: str = Depends(oauth2_scheme)):
    decoded_token = decode_access_token(token=jwt_token)
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
    return db.query(UserModel).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.UserId == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.Email == email).first()

def add_user(db: Session, user: UserRequest):
    salt = bcrypt.gensalt()
    password_bytes = user.password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    db_user = UserModel(
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