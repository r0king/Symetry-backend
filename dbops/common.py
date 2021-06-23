"""
Common utilities for database operations
"""
from sqlalchemy.orm import Session
from database.config_db import Base


def commit_changes_to_object(database: Session, obj: Base):
    """Finish the database transaction and refresh session"""
    database.add(obj)
    database.commit()
    database.refresh(obj)
