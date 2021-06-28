"""
CRUD The Apps table
"""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.models import App
from schemas.apps import CreateApp, UpdateApp
from .common import commit_changes_to_object, list_table


def create_app(database: Session, app: CreateApp):
    """To create a new entry"""
    database_app=App(**app.dict())
    if database_app:
        raise HTTPException(status_code=409, detail="App already registered.")

    commit_changes_to_object(database, database_app)
    return database_app


def get_app_by_id(database: Session, app_id: int):
    """Get App By ID"""
    return database.query(App).filter_by(id=app_id).first()


def delete_app(database: Session, app_id: str):
    """To delete an app entry"""
    db_app = get_app_by_id(database, app_id)

    if db_app is None:
        raise HTTPException(status_code=409, detail="App not found.")

    database.delete(db_app)
    database.commit()
    database.refresh()


def update_app(database: Session, updated_app: UpdateApp, app_id: str):
    """To update the app profile"""
    db_app = get_app_by_id(database, app_id)

    if db_app is None:
        raise HTTPException(status_code=409, detail="App not found.")

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
