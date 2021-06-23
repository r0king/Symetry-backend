from sqlalchemy.orm import Session
from dbops.common import commit_changes_to_object
from database.models import Session as SessionTable
from database.datamodels import SessionCreate


def get_token_id_by_app_id(
        db: Session,
        app_id: int):       # get token id with app id
                            
    return db.query(SessionTable).filter_by(SessionTable.app_id == app_id).all()


def get_token_id_by_user_id(
        db: Session,
        user_id: int):      # get token id with user id

    return db.query(SessionTable).filter_by(SessionTable.user_id == user_id).all()


def create_token_id(
        database: Session,
        session: SessionCreate,        
       
        # app_id: int,
        # user_id: int
       
        ):      # create session with user id

    user_session = SessionTable(**session.dict()) #, app_id=app_id, user_id=user_id)
    commit_changes_to_object(database, user_session)

    return user_session
