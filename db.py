import os

import sqlitecloud
from dotenv import load_dotenv

load_dotenv()
SQLITE_PROJECT_ID = os.getenv("SQLITE_PROJECT_ID")
SQLITE_HOST_PORT = os.getenv("SQLITE_HOST_PORT")
SQLITE_DATABASE_NAME = os.getenv("SQLITE_DATABASE_NAME")
SQLITE_API_KEY = os.getenv("SQLITE_API_KEY")


conn = sqlitecloud.connect(f"sqlitecloud://{SQLITE_PROJECT_ID}.sqlite.cloud:{SQLITE_HOST_PORT}/{SQLITE_DATABASE_NAME}?apikey={SQLITE_API_KEY}")

cursor = conn.execute("SELECT * FROM users WHERE user_id = ?", (4, ))
result = cursor.fetchone()

print(result)

conn.close()