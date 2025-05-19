from pydantic import BaseModel
from datetime import date, datetime
from enums.enums import RolesEnum, SessionStatusEnum, AttendanceStatusEnum

class UserResponse(BaseModel):
    user_id: int
    role: RolesEnum
    first_name: str
    last_name: str
    email: str
    password: str

class GroupResponse(BaseModel):
    group_id: int
    code: str

class CourseResponse(BaseModel):
    course_id: int
    name: str
    professor_name: str

class CourseGroupResponse(BaseModel):
    course_group_id: int
    course_id: int
    group_id: int

class StudentGroupResponse(BaseModel):
    id: int
    student_id: int
    group_id: int

class SessionResponse(BaseModel):
    session_id: int
    course_id: int
    room: str
    date: date
    start_time: datetime
    end_time: datetime
    status: SessionStatusEnum

class AttendanceResponse(BaseModel):
    attendance_id: int
    session_id: int
    student_id: int
    time: datetime
    status: AttendanceStatusEnum
