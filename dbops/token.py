from sqlalchemy.orm import Token
from dbops.common import commit_changes_to_object
from database.models import Token
from database.datamodels import TokenSchema


def get_token_id(
        db: Token,
        Token: TokenSchema):        # get token id 

    return db.query(Token).filter(Token.user_id == session.user_id, Token.app_id == session.app_id).first()


def get_token_id_by_app_id(
        db: Token,
        app_id: int):                   # get token id with app id

    return db.query(Token).filter_by(app_id == app_id)


def get_token_id_by_user_id(
        db:Token,
        user_id: int):                  # get token id with user id

    return db.query(Token).filter_by(user_id == user_id)


def create_token_id(
        db: Token,
        token: TokenSchema):        # create session with user id

    user_session = Token(**session.dict())
    commit_changes_to_object(database, user_session)

    return user_session
def delete_token(
        db: Token,
        token: TokenSchema):        # delete token id 

    query = db.query(Token).filter(Token.user_id == session.user_id, Token.app_id == session.app_id).first()
    db.delete(query)
    db.commit()
    db.refresh(query)
    return query
