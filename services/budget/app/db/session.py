# /services/budget/app/db/session.py
from sqlalchemy import create_engine
from app.core.config import settings
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = "sqlite:///./budget.db"
SQLALCHEMY_DATABASE_URL = settings.budget_database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
