from urllib import request

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from enums.db_enums import RolesEnum
from schemas.schemas import GenericResponse, UserResponse, UserRequest, TokenData
from services import service
from db.db import get_database_session
from services.service import jwt_validation_response, hash_password

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# C - Create Operations
# Add User Entity.
@user_router.post("/add_user/", response_model=GenericResponse[UserResponse])
async def add_user(user: UserRequest, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if RolesEnum.admin != jwt_token_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action."
        )
    if service.validate_user(user=user, db=db):
        db_user = service.add_user(db=db, user=user)
        response = GenericResponse(
            status_code=status.HTTP_201_CREATED,
            message="User added successfully.",
            data=db_user
        )
    else:
        response = GenericResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="User not added successfully."
        )
    return response


# R - Read Operations
# Get all Users.
@user_router.get("/", response_model=GenericResponse[list[UserResponse]])
async def get_all_users(jwt_token: TokenData = Depends(jwt_validation_response), skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if RolesEnum.admin != jwt_token_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action.",
            headers = {
                "WWW-Authenticate": "Bearer"
            },
        )

    users = service.get_all_users(skip=skip, limit=limit, db=db)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found.")

    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="Users retrieved successfully",
        data=users
    )
    return response

# Get User by UserID
@user_router.get("/id={user_id}", response_model=GenericResponse[UserResponse])
async def get_user_by_id(user_id: int, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if RolesEnum.admin != jwt_token_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action.",
            headers = {
                "WWW-Authenticate": "Bearer"
            },
        )

    user = service.get_user_by_id(user_id=user_id, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="User retrieved successfully",
        data=user
    )
    return response

# Get User by Email
@user_router.get("/email={email}", response_model=GenericResponse[UserResponse])
async def get_user_by_email(email: str, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if RolesEnum.admin != jwt_token_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action.",
            headers = {
                "WWW-Authenticate": "Bearer"
            },
        )
    if email == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email cannot be empty."
        )
    user = service.get_user_by_email(email=email, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="User retrieved successfully",
        data=user
    )
    return response

# U - Update
# Update single User
@user_router.put("/update_user/id={user_id}", response_model=GenericResponse[UserResponse])
async def update_user(user_id: int, user: UserRequest, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if RolesEnum.admin != jwt_token_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action.",
            headers = {
                "WWW-Authenticate": "Bearer"
            },
        )
    db_user = service.get_user_by_id(user_id=user_id, db=db)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    db_user.FirstName = user.first_name if user.first_name != "" else db_user.FirstName
    db_user.LastName = user.last_name if user.last_name != "" else db_user.LastName
    db_user.Email = user.email if user.email != "" else db_user.Email
    db_user.Password = hash_password(user.password) if user.password != "" else db_user.Password
    db_user.Role = user.role if user.role != "" else db_user.Role
    db.commit()

    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="User updated successfully.",
        data=db_user
    )
    return response

# D - Delete
# Delete single User
@user_router.delete("/delete_user/id={user_id}", response_model=GenericResponse[UserResponse])
async def delete_user(user_id: int, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if RolesEnum.admin != jwt_token_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action.",
            headers = {
                "WWW-Authenticate": "Bearer"
            },
        )
    db_user = service.get_user_by_id(user_id=user_id, db=db)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    db.delete(db_user)
    db.commit()
    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="User deleted successfully.",
        data=db_user
    )
    return response