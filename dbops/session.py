from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.sql.expression import desc
from dbops.common import commit_changes_to_object
from database.models import Session as SessionTable
from database.datamodels import SessionSchema


def list_sessions(
        db: Session,
        session:  SessionSchema
        
        ):        # get all sessions of user

    return db.query(SessionTable).filter(or_(SessionTable.user_id == session.user_id, SessionTable.id == session.id))\
    .order_by(desc(SessionTable.timestamp)).all()

def get_session_by_id(
        db: Session,
        id:  int):        # get session id

    return db.query(SessionTable).filter_by(id == id)


def delete_session(
        db: Session,
        session: SessionSchema):
                                        # delete session 
    query = db.query(SessionTable).filter_by(SessionTable.user_id ==
                                          session.user_id, SessionTable.id == session.id)
    db.delete(query)
    db.commit()
    db.refresh(query)

    return query


def create_session(
        database: Session,
        session: SessionSchema):        # create session with user id

    user_session = SessionTable(**session.dict())
    commit_changes_to_object(database, user_session)

    return user_session
