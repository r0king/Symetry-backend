"""
CRUD tokens table
"""
from sqlalchemy.orm.session import Session
from dbops.common import commit_changes_to_object, list_table
from database.models import Token
from schemas.tokens import TokenCreate


def get_token_by_id(database: Session, token_id: str):
    """
    Get token by id
    """
    return database.query(Token).filter_by(token_id=token_id).first()


def list_tokens(database: Session, **kwargs):
    """
    List tokens

    Same Params as for common.list_table
    """
    return list_table(database, Token, **kwargs)


def create_token(database: Session, token_data: TokenCreate):
    """
    Create token in db
    """
    db_token = Token(**token_data.dict())
    commit_changes_to_object(database, db_token)


def delete_token(database: Session, token_id: str):
    """
    Delete token from database
    """
    db_token = get_token_by_id(database, token_id)
    database.delete(db_token)
    database.commit()
    database.refresh()
