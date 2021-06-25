from sqlalchemy.orm import Session
from dbops.common import commit_changes_to_object
from database.models import Token
from database.datamodels import TokenSchema


def get_token_id(
        db: Session,
        session: TokenSchema):        # get token id 

    return db.query(Token).filter(Token.user_id == session.user_id, Token.app_id == session.app_id).first()


def get_token_id_by_app_id(
        db: Session,
        app_id: int):                   # get token id with app id

    return db.query(Token).filter_by(app_id == app_id).all()


def get_token_id_by_user_id(
        db: Session,
        user_id: int):                  # get token id with user id

    return db.query(Token).filter_by(user_id == user_id).all()


def create_token_id(
        database: Session,
        session: TokenSchema):        # create session with user id

    user_session = Token(**session.dict())
    commit_changes_to_object(database, user_session)

    return user_session
