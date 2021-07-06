"""
CRUD The Apps table
"""
from app.exceptions import IntendedException
from sqlalchemy.orm import Session
from app.database.models import App
from app.schemas.apps import CreateApp, UpdateApp
from .common import commit_changes_to_object, hash_string, list_table


def create_app(database: Session, app: CreateApp):
    """To create a new entry"""
    app.secret = hash_string(app.secret)
    database_app=App(**app.dict())

    commit_changes_to_object(database, database_app)
    return database_app


def get_app_by_id(database: Session, app_id: str):
    """Get App By ID"""
    return database.query(App).filter_by(id=app_id).first()

def get_app_by_user_id(database: Session, user_id: str):
    """Get App By ID"""
    return database.query(App).filter_by(user_id=user_id).first()

def delete_app(database: Session, app_id: str):
    """To delete an app entry"""
    db_app = get_app_by_id(database, app_id)

    if db_app is None:
        raise IntendedException("App not found")

    database.delete(db_app)
    database.commit()


def update_app(database: Session, updated_app: UpdateApp, app_id: str):
    """To update the app profile"""
    db_app = get_app_by_id(database, app_id)

    if db_app is None:
        raise IntendedException("App not found")

    for name, entry in vars(updated_app.dict(exclude_none=True)):
        setattr(db_app, name, entry)

    commit_changes_to_object(database, db_app)
    return db_app


def list_apps(database: Session, **kwargs):
    """
    List Apps

    Same Params as for common.list_table
    """
    return list_table(database, App, **kwargs)
