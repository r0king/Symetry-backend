"""
CRUD the session table
"""
from hashlib import sha256
from sqlalchemy.orm import Session
from database.models import Session as SessionTable
from schemas.sessions import SessionCreate
from .common import commit_changes_to_object, list_table


def list_sessions(database: Session, **kwargs):
    """
    List sessions

    Same Params as for common.list_table
    """
    return list_table(database, SessionTable, **kwargs)


def get_session_by_id(database: Session, session_id: int):
    """
    Get Sesison uniquely by id
    """
    return database.query(SessionTable).filter_by(id=session_id).first()


def delete_session(database: Session, session_id: int):
    """
    Delete Session
    """
    session_in_db = get_session_by_id(database, session_id)
    database.delete(session_in_db)
    database.commit()
    database.refresh()

    return session_in_db


def create_session(database: Session, token: str, session: SessionCreate):
    """
    Create Session
    """
    user_session = SessionTable(**session.dict(),token=sha256(token))
    commit_changes_to_object(database, user_session)

    return user_session
