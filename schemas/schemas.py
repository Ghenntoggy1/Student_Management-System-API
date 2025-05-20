from pydantic import BaseModel, Field
from datetime import date as _date, datetime as _datetime
from enums.db_enums import RolesEnum, SessionStatusEnum, AttendanceStatusEnum
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = Field(default='bearer')

class TokenData(BaseModel):
    sub: str
    name: str
    role: RolesEnum
    iat: int
    exp: int

class GenericResponse(BaseModel, Generic[T]):
    status_code: int
    message: str
    data: Optional[T] = None

class UserResponse(BaseModel):
    user_id: int = Field(..., alias='UserId')
    role: RolesEnum = Field(..., alias='Role')
    first_name: str = Field(..., alias='FirstName')
    last_name: str = Field(..., alias='LastName')
    email: str = Field(..., alias='Email')
    password: str = Field(..., alias='Password')

class UserRequest(BaseModel):
    role: Optional[RolesEnum] = Field(..., alias='Role')
    first_name: Optional[str] = Field(..., alias='FirstName')
    last_name: Optional[str] = Field(..., alias='LastName')
    email: Optional[str] = Field(..., alias='Email')
    password: Optional[str] = Field(..., alias='Password')

class GroupResponse(BaseModel):
    group_id: int = Field(..., alias='GroupId')
    name: str = Field(..., alias='Name')

class CourseResponse(BaseModel):
    course_id: int = Field(..., alias='CourseId')
    name: str = Field(..., alias='Name')
    professor_id: str = Field(..., alias='ProfessorId')

class CourseGroupResponse(BaseModel):
    id: int = Field(..., alias='id')
    course_id: int = Field(..., alias='CourseId')
    group_id: int = Field(..., alias='GroupId')

class StudentGroupResponse(BaseModel):
    id: int = Field(..., alias='id')
    student_id: int = Field(..., alias='StudentId')
    group_id: int = Field(..., alias='GroupId')

class SessionResponse(BaseModel):
    session_id: int = Field(..., alias='SessionId')
    course_id: int = Field(..., alias='CourseId')
    room: str = Field(..., alias='Room')
    date: _date = Field(..., alias='Date')
    start_time: _datetime = Field(..., alias='StartTime')
    end_time: _datetime = Field(..., alias='EndTime')
    status: SessionStatusEnum = Field(..., alias='Status')

class AttendanceResponse(BaseModel):
    attendance_id: int = Field(..., alias='AttendanceId')
    session_id: int = Field(..., alias='SessionId')
    student_id: int = Field(..., alias='StudentId')
    time: _datetime = Field(..., alias='Time')
    status: AttendanceStatusEnum = Field(..., alias='Status')
