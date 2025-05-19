import os
import sqlitecloud
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
SQLITE_PROJECT_ID = os.getenv("SQLITE_PROJECT_ID")
SQLITE_HOST_PORT = os.getenv("SQLITE_HOST_PORT")
SQLITE_DATABASE_NAME = os.getenv("SQLITE_DATABASE_NAME")
SQLITE_API_KEY = os.getenv("SQLITE_API_KEY")

engine = create_engine(f"sqlitecloud://{SQLITE_PROJECT_ID}.sqlite.cloud:{SQLITE_HOST_PORT}/{SQLITE_DATABASE_NAME}?apikey={SQLITE_API_KEY}")

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()