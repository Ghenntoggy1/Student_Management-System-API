from db.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String


class CourseModel(Base):
    __tablename__ = 'courses'

    CourseId = Column(name='course_id', type_=Integer, primary_key=True)
    Name = Column(name='name', type_=String)
    ProfessorId = Column(ForeignKey('users.user_id'), name='professor_id', type_=Integer)
    # ProfessorId = Column('professor_id', Integer, ForeignKey('users.user_id'))