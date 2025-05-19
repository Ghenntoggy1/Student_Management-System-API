from db import Base
from sqlalchemy import Column, ForeignKey, Integer, String


class User(Base):
    __tablename__ = 'users'

    UserId = Column(Integer, primary_key=True, autoincrement=True)
    Role = Column(String)
    FirstName = Column(String)
    LastName = Column(String)
    Email = Column(String)
    Password = Column(String)

class Group(Base):
    __tablename__ = 'groups'

    GroupId = Column(Integer, primary_key=True, autoincrement=True)
    Code = Column(String)

class Course(Base):
    __tablename__ = 'courses'

    CourseId = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    ProfessorId = Column(Integer, ForeignKey('users.UserId'))

class CourseGroup(Base):
    __tablename__ = 'courses_groups'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    CourseId = Column(Integer, ForeignKey('courses.CourseId'))
    GroupId = Column(Integer, ForeignKey('groups.GroupId'))

class StudentGroup(Base):
    __tablename__ = 'students_groups'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    StudentId = Column(Integer, ForeignKey('users.UserId'))
    GroupId = Column(Integer, ForeignKey('groups.GroupId'))

class Session(Base):
    __tablename__ = 'sessions'

    SessionId = Column(Integer, primary_key=True, autoincrement=True)
    CourseId = Column(Integer, ForeignKey('courses.CourseId'))
    Room = Column(String)
    Date = Column(String)
    StartTime = Column(String)
    EndTime = Column(String)
    Status = Column(String)

class Attendance(Base):
    __tablename__ = 'attendances'

    AttendanceId = Column(Integer, primary_key=True, autoincrement=True)
    SessionId = Column(Integer, ForeignKey('sessions.SessionId'))
    StudentId = Column(Integer, ForeignKey('users.UserId'))
    Time = Column(String)
    Status = Column(String)
