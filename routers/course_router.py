from urllib import request

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from enums.db_enums import RolesEnum
from models.user_model import UserModel
from schemas.schemas import GenericResponse, UserResponse, UserRequest, TokenData, CourseResponse, CourseRequest
from services import service
from db.db import get_database_session
from services.service import jwt_validation_response, hash_password

course_router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

# C - Create
# Add Course Entity.
@course_router.post("/add_course/", response_model=GenericResponse[CourseResponse])
async def add_course(course: CourseRequest, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if jwt_token_role not in [RolesEnum.admin, RolesEnum.professor]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action."
        )
    if service.validate_course(course=course, db=db):
        db_course = service.add_course(db=db, course=course)
        response = GenericResponse(
            status_code=status.HTTP_201_CREATED,
            message="Course added successfully.",
            data=db_course
        )
    else:
        response = GenericResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Course not added successfully."
        )
    return response

# R - Read
# Get all Courses.
@course_router.get("/", response_model=GenericResponse[list[CourseResponse]])
async def get_all_courses(jwt_token: TokenData = Depends(jwt_validation_response), skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if jwt_token_role not in [RolesEnum.admin, RolesEnum.professor, RolesEnum.student]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action.",
            headers = {
                "WWW-Authenticate": "Bearer"
            },
        )
    courses = service.get_all_courses(skip=skip, limit=limit, db=db)
    if not courses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No courses found."
        )

    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="Courses retrieved successfully",
        data=courses
    )
    return response

# U - Update
# Update single Course
@course_router.put("/update_course/id={course_id}", response_model=GenericResponse[CourseResponse])
async def update_course(course_id: int, course: CourseRequest, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if jwt_token_role not in [RolesEnum.admin, RolesEnum.professor]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )
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
    db_course = service.get_course_by_id(course_id=course_id, db=db)
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found."
        )

    db_course.Name = course.name if course.name != "" else db_course.Name
    db_course.ProfessorId = course.professor_id if course.professor_id != "" else db_course.ProfessorId
    db.commit()
    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="Course updated successfully.",
        data=db_course
    )
    return response

# D - Delete
# Delete single Course
@course_router.delete("/delete_course/id={course_id}", response_model=GenericResponse[CourseResponse])
async def delete_course(course_id: int, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if jwt_token_role not in [RolesEnum.admin, RolesEnum.professor]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )
    db_course = service.get_course_by_id(course_id=course_id, db=db)
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found."
        )
    db.delete(db_course)
    db.commit()
    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="Course deleted successfully.",
        data=db_course
    )
    return response