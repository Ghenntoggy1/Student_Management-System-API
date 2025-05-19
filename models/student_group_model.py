from db.db import Base
from sqlalchemy import Column, ForeignKey, Integer


class StudentGroupModel(Base):
    __tablename__ = 'students_groups'

    Id = Column(name='id', type_=Integer, primary_key=True)
    StudentId = Column(ForeignKey('users.user_id'), name='student_id', type_=Integer)
    GroupId = Column(ForeignKey('groups.group_id'), name='group_id', type_=Integer)
    # StudentId = Column('student_id', Integer, ForeignKey('users.user_id'))
    # GroupId = Column('group_id', Integer, ForeignKey('groups.group_id')