from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db.db import SessionLocal
from services import service
from db import schemas
import auth.auth as auth_layer
from enums.enums import RolesEnum

app = FastAPI()

def get_database_session():
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()

@app.get("/")
async def root():
    return {"message": "Welcome to Student Management System!"}

@app.post("/login/", response_model=schemas.Token)
async def login(user: schemas.UserLogin, db: Session = Depends(get_database_session)):
    user_obj = service.get_user_by_email(email=user.email, db=db)
    if not user_obj:
        return {"message": "Invalid credentials"}

    if not auth_layer.verify_password(user.password, user_obj.Password):
        return {"message": "Invalid credentials"}

    access_token = auth_layer.create_access_token(data={"sub": user_obj.Email, "role": user_obj.Role})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/", response_model=list[schemas.UserResponse])
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    users = service.get_all_users(skip=skip, limit=limit, db=db)
    return users

@app.post("/add_user/", response_model=schemas.UserResponse)
async def add_user(user: schemas.UserRequest, jwt_token: schemas.Token, db: Session = Depends(get_database_session)):
    decoded_token: dict = auth_layer.decode_access_token(token=jwt_token.access_token)
    jwt_token_role: schemas.RolesEnum = decoded_token.get("role")
    if RolesEnum.admin != jwt_token_role:
        return {"message": "You don't have permission to add a user"}

    return service.add_user(db=db, user=user)
