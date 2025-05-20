from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from enums.db_enums import RolesEnum
from schemas.schemas import GenericResponse, TokenData, AttendanceRequest, AttendanceResponse
from services import service
from db.db import get_database_session
from services.service import jwt_validation_response, validate_attendance

attendance_router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)

# C - Create
# Add Attendance Entity.
@attendance_router.post("/add_attendance/", response_model=GenericResponse[AttendanceResponse])
async def add_attendance(attendance: AttendanceRequest, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if jwt_token_role not in [RolesEnum.admin, RolesEnum.professor]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action."
        )
    if validate_attendance(attendance=attendance, db=db):
        db_attendance = service.add_attendance(db=db, attendance=attendance)
        response = GenericResponse(
            status_code=status.HTTP_201_CREATED,
            message="Attendance added successfully.",
            data=db_attendance
        )
    else:
        response = GenericResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Attendance not added successfully."
        )
    return response

# R - Read
# Get all Attendances.
@attendance_router.get("/", response_model=GenericResponse[list[AttendanceResponse]])
async def get_all_attendances(jwt_token: TokenData = Depends(jwt_validation_response), skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if jwt_token_role not in [RolesEnum.admin, RolesEnum.professor, RolesEnum.student]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action.",
            headers = {
                "WWW-Authenticate": "Bearer"
            },
        )
    attendances = service.get_all_attendances(skip=skip, limit=limit, db=db)
    if not attendances:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No attendances found."
        )
    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="Attendances retrieved successfully",
        data=attendances
    )
    return response

# U - Update
# Update single Attendance by Student ID and Date
@attendance_router.put("/update_attendance/student_id={student_id}&date={date}", response_model=GenericResponse[AttendanceResponse])
async def update_attendance(student_id: int, date: str, attendance: AttendanceRequest, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if jwt_token_role not in [RolesEnum.admin, RolesEnum.professor]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    if not validate_attendance(attendance=attendance, db=db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance not updated successfully."
        )
    db_attendance = service.get_attendance_by_student_id_and_date(student_id=student_id, date=date, db=db)
    if not db_attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance not found."
        )
    db_attendance.Status = attendance.status if attendance.status != "" else db_attendance.Status
    db.commit()
    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="Attendance updated successfully.",
        data=db_attendance
    )
    return response

# D - Delete
# Delete single Attendance by Student ID and Date
@attendance_router.delete("/delete_attendance/student_id={student_id}&date={date}", response_model=GenericResponse[AttendanceResponse])
async def delete_attendance(student_id: int, date: str, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if jwt_token_role not in [RolesEnum.admin, RolesEnum.professor]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )
    db_attendance = service.get_attendance_by_student_id_and_date(student_id=student_id, date=date, db=db)
    if not db_attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance not found."
        )
    db.delete(db_attendance)
    db.commit()
    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="Attendance deleted successfully.",
        data=db_attendance
    )
    return response
