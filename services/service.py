from fastapi import HTTPException, Depends
from starlette import status
import bcrypt
from sqlalchemy.orm import Session

from enums.db_enums import RolesEnum, SessionStatusEnum
from models.user_model import UserModel
from models.group_model import GroupModel
from models.session_model import SessionModel
from models.course_model import CourseModel
from models.attendance_model import AttendanceModel
from models.course_group_model import CourseGroupModel
from models.student_group_model import StudentGroupModel
from schemas.schemas import Token, UserRequest, UserResponse, CourseRequest, SessionRequest, AttendanceRequest
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

def validate_user(user: UserRequest, db: Session):
    if user.first_name == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="First name cannot be empty."
        )
    if user.last_name == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last name cannot be empty."
        )
    if user.email == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email cannot be empty."
        )
    if user.password == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password cannot be empty."
        )
    if user.role == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role cannot be empty."
        )
    if get_user_by_email(db=db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )
    return True

def validate_course(course: CourseRequest, db: Session):
    if course.name == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course name cannot be empty."
        )
    if course.professor_id == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course professor cannot be empty."
        )
    if db.query(CourseModel).filter(CourseModel.Name == course.name).first() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course with this name already exists."
        )
    if db.query(UserModel).filter(UserModel.UserId == course.professor_id).first() is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course professor does not exist."
        )
    if db.query(UserModel).filter(UserModel.UserId == course.professor_id).first().Role != RolesEnum.professor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This User is not a professor."
        )
    return True

def validate_session(session: SessionRequest, db: Session):
    if session.course_id == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course id cannot be empty."
        )
    if session.room == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room cannot be empty."
        )
    if session.date == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Date cannot be empty."
        )
    if session.start_time == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time cannot be empty."
        )
    if session.end_time == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time cannot be empty."
        )
    if db.query(CourseModel).filter(CourseModel.CourseId == session.course_id).first() is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course with this id does not exist."
        )
    return True

def validate_attendance(attendance: AttendanceRequest, db: Session):
    if attendance.session_id == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session id cannot be empty."
        )
    if attendance.student_id == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student id cannot be empty."
        )
    if attendance.time == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Time cannot be empty."
        )
    if attendance.status == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status cannot be empty."
        )
    if get_user_by_id(db=db, user_id=attendance.student_id) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student with this id does not exist."
        )
    if get_user_by_id(db=db, user_id=attendance.student_id).Role != RolesEnum.student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This User is not a student."
        )
    if db.query(SessionModel).filter(SessionModel.SessionId == attendance.session_id).first() is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session with this id does not exist."
        )
    return True

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

def add_course(db: Session, course: CourseRequest):
    db_course = CourseModel(
        Name=course.name,
        ProfessorId=course.professor_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_all_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CourseModel).offset(skip).limit(limit).all()

def get_course_by_id(db: Session, course_id: int):
    return db.query(CourseModel).filter(CourseModel.CourseId == course_id).first()

def add_session(db: Session, session: SessionRequest):
    db_session = SessionModel(
        CourseId=session.course_id,
        Room=session.room,
        Date=session.date.strftime("%Y-%m-%d"),
        StartTime=session.start_time.strftime("%H:%M"),
        EndTime=session.end_time.strftime("%H:%M"),
        Status=SessionStatusEnum.not_started

    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_all_sessions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SessionModel).offset(skip).limit(limit).all()

def get_session_by_id(db: Session, session_id: int):
    return db.query(SessionModel).filter(SessionModel.SessionId == session_id).first()

def add_attendance(db: Session, attendance: AttendanceRequest):
    db_attendance = AttendanceModel(
        SessionId=attendance.session_id,
        StudentId=attendance.student_id,
        Time=attendance.time.strftime("%H:%M"),
        Status=attendance.status
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def get_all_attendances(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AttendanceModel).offset(skip).limit(limit).all()

def get_attendance_by_student_id_and_date(db: Session, student_id: int, date: str):
    session = db.query(SessionModel).filter(SessionModel.Date == date).first()
    if not session:
        return None
    else:
        return db.query(AttendanceModel).filter(AttendanceModel.StudentId == student_id, AttendanceModel.SessionId == session.SessionId).first()

def hash_password(password: str):
    salt = bcrypt.gensalt()
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    return hashed_password