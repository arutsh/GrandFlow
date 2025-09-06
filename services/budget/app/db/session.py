# /services/budget/app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# SQLALCHEMY_DATABASE_URL = "sqlite:///./budget.db"
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://budget:budget_pass@budget-db:5432/budget_db"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
