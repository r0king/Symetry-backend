"""
Main dependancies
"""
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from app.database.config_db import SessionLocal
from app.schemas.users import User
from app.schemas.apps import App
from app.dbops.sessions import get_session_by_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


def get_db():
    """
    Get the current db session
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def get_current_user(database: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    :return: schemas.User
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    session = get_session_by_token(database, token)

    if session is None:
        raise credentials_exception

    return User(**session.user.__dict__)

def get_current_app(database: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    :return: schemas.App
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    session = get_session_by_token(database, token)

    if session is None:
        raise credentials_exception

    return App(**session.app.__dict__)