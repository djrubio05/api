from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine
from .config import settings

SQL_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQL_DATABASE_URL)

def get_session():
    with Session(engine, autocommit=False, autoflush=False) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


# import psycopg
# import time
# from psycopg.rows import dict_row
# while True:

#     try:
#         conn = psycopg.connect(host = 'localhost', dbname = "api", user = "postgres", 
#                              password = "2545",row_factory=dict_row)
#         cur = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
