from sqlalchemy.orm import Session
from sqlalchemy import or_
from dbops.common import commit_changes_to_object
from database.models import Session as SessionTable
from database.datamodels import SessionSchema


def get_session(
        db: Session,
        session:  SessionSchema):        # get token id with app id

    return db.query(SessionTable).filter_by(or_(SessionTable.user_id == session.user_id, SessionTable.id == session.session_id))


def create_session(
        database: Session,
        session: SessionSchema):        # create session with user id

    user_session = SessionTable(**session.dict())
    commit_changes_to_object(database, user_session)

    return user_session
