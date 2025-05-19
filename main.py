from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db.db import SessionLocal
from services import service
from db import schemas


app = FastAPI()

def get_database_session():
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users/", response_model=list[schemas.UserResponse])
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    users = service.get_all_users(skip=skip, limit=limit, db=db)
    return users

@app.post("/add_user/", response_model=schemas.UserResponse)
async def add_user(user: schemas.UserRequest, db: Session = Depends(get_database_session)):
    return service.add_user(db=db, user=user)
