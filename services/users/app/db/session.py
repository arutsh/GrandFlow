# /services/users/app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://users:users_pass@users-db:5432/users_db"
)


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
