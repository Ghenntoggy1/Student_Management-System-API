from db import Base
from sqlalchemy import Column, ForeignKey, Integer, String


class User(Base):
    __tablename__ = 'users'

    UserId = Column(name='user_id', type_=Integer, primary_key=True)
    Role = Column(name='role', type_=String)
    FirstName = Column(name='first_name', type_=String)
    LastName = Column(name='last_name', type_=String)
    Email = Column(name='email', type_=String)
    Password = Column(name='password', type_=String)

class Group(Base):
    __tablename__ = 'groups'

    GroupId = Column(name='group_id', type_=Integer, primary_key=True)
    Code = Column(name='code', type_=String)

class Course(Base):
    __tablename__ = 'courses'

    CourseId = Column(name='course_id', type_=Integer, primary_key=True)
    Name = Column(name='name', type_=String)
    ProfessorId = Column(ForeignKey('users.user_id'), name='professor_id', type_=Integer)
    # ProfessorId = Column('professor_id', Integer, ForeignKey('users.user_id'))

class CourseGroup(Base):
    __tablename__ = 'courses_groups'

    Id = Column(name='id', type_=Integer, primary_key=True)
    CourseId = Column(ForeignKey('courses.course_id'), name='course_id', type_=Integer)
    GroupId = Column(ForeignKey('groups.group_id'), name='group_id', type_=Integer)
    # CourseId = Column('course_id', Integer, ForeignKey('courses.course_id'))
    # GroupId = Column('group_id', Integer, ForeignKey('groups.group_id')

class StudentGroup(Base):
    __tablename__ = 'students_groups'

    Id = Column(name='id', type_=Integer, primary_key=True)
    StudentId = Column(ForeignKey('users.user_id'), name='student_id', type_=Integer)
    GroupId = Column(ForeignKey('groups.group_id'), name='group_id', type_=Integer)
    # StudentId = Column('student_id', Integer, ForeignKey('users.user_id'))
    # GroupId = Column('group_id', Integer, ForeignKey('groups.group_id')

class Session(Base):
    __tablename__ = 'sessions'

    SessionId = Column(name='session_id', type_=Integer, primary_key=True)
    CourseId = Column(ForeignKey('courses.course_id'), name='course_id', type_=Integer)
    # CourseId = Column('course_id', Integer, ForeignKey('courses.course_id'))
    Room = Column(name='room', type_=String)
    Date = Column(name='date', type_=String)
    StartTime = Column(name='start_time', type_=String)
    EndTime = Column(name='end_time', type_=String)
    Status = Column(name='status', type_=String)

class Attendance(Base):
    __tablename__ = 'attendances'

    AttendanceId = Column(name='attendance_id', type_=Integer, primary_key=True)
    SessionId = Column(ForeignKey('sessions.session_id'), name='session_id', type_=Integer)
    StudentId = Column(ForeignKey('users.user_id'), name='student_id', type_=Integer)
    # SessionId = Column('session_id', Integer, ForeignKey('sessions.session_id'))
    # StudentId = Column('student_id', Integer, ForeignKey('users.user_id')
    Time = Column(name='time', type_=String)
    Status = Column(name='status', type_=String)
