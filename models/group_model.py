from db.db import Base
from sqlalchemy import Column, Integer, String


class GroupModel(Base):
    __tablename__ = 'groups'

    GroupId = Column(name='group_id', type_=Integer, primary_key=True)
    Code = Column(name='code', type_=String)