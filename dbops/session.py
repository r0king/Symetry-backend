from sqlalchemy.orm import Session
from dbops.common import commit_changes_to_object
from database.models import Session as SessionTable
from database.datamodels import  SessionSchema


def get_token(
        db: Session,
        session:  SessionSchema):        # get token id

    return db.query(SessionTable).filter(SessionTable.user_id == session.user_id, SessionTable.app_id == session.app_id).first()


def get_session(
        db: Session,
        user_id: int):                  # get token id with user id

    return db.query(SessionTable).filter_by(user_id == user_id)

def get_session_by_session_id(
        db: Session,
        session_id: int):                   # get token id with app id

    return db.query(SessionTable).filter_by(SessionTable.id == session_id)



def create_session(
        database: Session,
        session: SessionSchema):        # create session with user id

    user_session = SessionTable(**session.dict())
    commit_changes_to_object(database, user_session)

    return user_session
