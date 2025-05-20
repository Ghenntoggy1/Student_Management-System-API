from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from enums.db_enums import RolesEnum
from models.user_model import UserModel
from schemas.schemas import GenericResponse, TokenData, CourseResponse, CourseRequest, SessionResponse, SessionRequest
from services import service
from db.db import get_database_session
from services.service import jwt_validation_response, validate_session

session_router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)

# C - Create
# Add Session Entity.
@session_router.post("/add_session/", response_model=GenericResponse[SessionResponse])
async def add_session(session: SessionRequest, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if jwt_token_role not in [RolesEnum.admin, RolesEnum.professor]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action."
        )
    if service.validate_session(session=session, db=db):
        db_session = service.add_session(db=db, session=session)
        response = GenericResponse(
            status_code=status.HTTP_201_CREATED,
            message="Session added successfully.",
            data=db_session
        )
    else:
        response = GenericResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Session not added successfully."
        )
    return response

# R - Read
# Get all Sessions.
@session_router.get("/", response_model=GenericResponse[list[SessionResponse]])
async def get_all_sessions(jwt_token: TokenData = Depends(jwt_validation_response), skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if jwt_token_role not in [RolesEnum.admin, RolesEnum.professor, RolesEnum.student]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action.",
            headers = {
                "WWW-Authenticate": "Bearer"
            },
        )
    sessions = service.get_all_sessions(skip=skip, limit=limit, db=db)
    if not sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No sessions found."
        )
    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="Sessions retrieved successfully",
        data=sessions
    )
    return response

# U - Update
# Update single Session
@session_router.put("/update_session/id={session_id}", response_model=GenericResponse[SessionResponse])
async def update_session(session_id: int, session: SessionRequest, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if jwt_token_role not in [RolesEnum.admin, RolesEnum.professor]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )
    if not validate_session(session=session, db=db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session not updated successfully."
        )
    db_session = service.get_session_by_id(session_id=session_id, db=db)
    if not db_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found."
        )

    db_session.CourseId = session.course_id if session.course_id != "" else db_session.CourseId
    db_session.Room = session.room if session.room != "" else db_session.StudentId
    db_session.Date = session.date.strftime("%Y-%m-%d") if session.date != "" else db_session.Date
    db_session.StartTime = session.start_time.strftime("%H:%M") if session.start_time != "" else db_session.StartTime
    db_session.EndTime = session.end_time.strftime("%H:%M") if session.end_time != "" else db_session.EndTime
    db_session.Status = session.status if session.status != "" else db_session.Status
    db.commit()
    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="Session updated successfully.",
        data=db_session
    )
    return response

# D - Delete
# Delete single Session
@session_router.delete("/delete_session/id={session_id}", response_model=GenericResponse[SessionResponse])
async def delete_session(session_id: int, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if jwt_token_role not in [RolesEnum.admin, RolesEnum.professor]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )
    db_session = service.get_session_by_id(session_id=session_id, db=db)
    if not db_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found."
        )
    db.delete(db_session)
    db.commit()
    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="Session deleted successfully.",
        data=db_session
    )
    return response