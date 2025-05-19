from db.db import Base
from sqlalchemy import Column, Integer, String


class UserModel(Base):
    __tablename__ = 'users'

    UserId = Column(name='user_id', type_=Integer, primary_key=True)
    Role = Column(name='role', type_=String)
    FirstName = Column(name='first_name', type_=String)
    LastName = Column(name='last_name', type_=String)
    Email = Column(name='email', type_=String)
    Password = Column(name='password', type_=String)
