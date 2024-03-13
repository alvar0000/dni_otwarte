from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2 # Wymagane przy pracy z PostgreSQL
from .db_properties import *


# Zmienne do łączenia się z bazą
username = get_username()
password = get_password()
host = get_host()
port = get_port()
database = get_database()


# URL bazy danych
DB_URL = f'postgresql://{username}:{password}@{host}:{port}/{database}'


# Obiekty do interakcji z bazą danych
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


# Funkcja do łączenia się z bazą
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
