from db.db import Base
from sqlalchemy import Column, ForeignKey, Integer


class CourseGroupModel(Base):
    __tablename__ = 'courses_groups'

    Id = Column(name='id', type_=Integer, primary_key=True)
    CourseId = Column(ForeignKey('courses.course_id'), name='course_id', type_=Integer)
    GroupId = Column(ForeignKey('groups.group_id'), name='group_id', type_=Integer)
    # CourseId = Column('course_id', Integer, ForeignKey('courses.course_id'))
    # GroupId = Column('group_id', Integer, ForeignKey('groups.group_id')