from db.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String

class AttendanceModel(Base):
    __tablename__ = 'attendances'

    AttendanceId = Column(name='attendance_id', type_=Integer, primary_key=True)
    SessionId = Column(ForeignKey('sessions.session_id'), name='session_id', type_=Integer)
    StudentId = Column(ForeignKey('users.user_id'), name='student_id', type_=Integer)
    # SessionId = Column('session_id', Integer, ForeignKey('sessions.session_id'))
    # StudentId = Column('student_id', Integer, ForeignKey('users.user_id')
    Time = Column(name='time', type_=String)
    Status = Column(name='status', type_=String)
