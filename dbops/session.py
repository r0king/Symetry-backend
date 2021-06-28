"""
CRUD the session table
"""
from hashlib import sha256
from sqlalchemy.orm import Session
from database.models import Session as SessionTable
from schemas.sessions import SessionCreate
from .common import commit_changes_to_object


def list_sessions(
    database: Session,
    identify_by: dict = dict,
    offset: int = 0,
    limit=None,
    order: str = "desc",
    sort_by: str = "timestamp"
):
    """
    List sessions

    :param limit: Limit the number of results
    :param identify_by: Dictionary of filters
    :param offset: Offset(Shift) the results by a certain value
    :param sort_by: Field to sort by
    :param order: asc for ascending, desc for descending
    """

    query = database.query(SessionTable).filter_by(**identify_by).offset(offset).\
        order_by("%s %s" % (sort_by, order))

    if limit:
        return {
            "count": query.count(),
            "results": query.limit(limit).all()
        }

    return {
        "count": query.count(),
        "results": query.all()
    }


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
