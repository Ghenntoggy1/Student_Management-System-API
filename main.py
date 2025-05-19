from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.db import SessionLocal
from services import service
from db.schemas import GenericResponse, UserLogin, UserRequest, Token
import auth.auth as auth_layer
from enums.enums import RolesEnum, JWTValidationResultsEnum

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

@app.post(path="/login/",
          response_model=GenericResponse)
async def login(user: UserLogin, db: Session = Depends(get_database_session)):
    user_obj = service.get_user_by_email(email=user.email, db=db)
    if not user_obj or not auth_layer.verify_password(user.password, user_obj.Password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials.")

    access_token = auth_layer.create_access_token(
        data={
            "sub": user_obj.Email,
            "name": user_obj.FirstName + " " + user_obj.LastName,
            "role": user_obj.Role,
        }
    )

    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="Login successful. Token is issued",
        data={
            "access_token": access_token,
            "token_type": "bearer"
        }
    )
    return response

@app.get("/users/", response_model=GenericResponse)
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    users = service.get_all_users(skip=skip, limit=limit, db=db)

    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="Users retrieved successfully",
        data=users
    )
    return response

@app.post("/add_user/", response_model=GenericResponse)
async def add_user(user: UserRequest, jwt_token: Token, db: Session = Depends(get_database_session)):
    decoded_token = service.jwt_validation_response(jwt_token)
    jwt_token_role: RolesEnum = decoded_token.get("role")
    if RolesEnum.admin != jwt_token_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action."
        )
    db_user = service.add_user(db=db, user=user)
    response = GenericResponse(
        status_code=status.HTTP_201_CREATED,
        message="User added successfully.",
        data=db_user
    )
    return response

