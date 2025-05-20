from db.db import Base
from sqlalchemy import Column, Integer, String


class UserModel(Base):
    __tablename__ = 'users'

    UserId = Column(name='user_id', type_=Integer, primary_key=True)
    Role = Column(name='role', type_=String, nullable=False)
    FirstName = Column(name='first_name', type_=String, nullable=False)
    LastName = Column(name='last_name', type_=String, nullable=False)
    Email = Column(name='email', type_=String, nullable=False, unique=True)
    Password = Column(name='password', type_=String, nullable=False)
