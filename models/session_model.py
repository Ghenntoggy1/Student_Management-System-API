from db.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String

class SessionModel(Base):
    __tablename__ = 'sessions'

    SessionId = Column(name='session_id', type_=Integer, primary_key=True)
    CourseId = Column(ForeignKey('courses.course_id'), name='course_id', type_=Integer)
    # CourseId = Column('course_id', Integer, ForeignKey('courses.course_id'))
    Room = Column(name='room', type_=String)
    Date = Column(name='date', type_=String)
    StartTime = Column(name='start_time', type_=String)
    EndTime = Column(name='end_time', type_=String)
    Status = Column(name='status', type_=String)