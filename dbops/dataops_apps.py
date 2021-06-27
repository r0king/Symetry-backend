from fastapi import FastAPI, HTTPException, applications
from sqlalchemy.orm import Session
from dbops.common import commit_changes_to_object
from database.models import App
from database.datamodels import CreateApp,updateApp
from sqlalchemy import update, func


def create_app(db:Session, app:CreateApp):
    """To create a new entry"""
    db_app=App(**app.dict())
    if db_app:
   	    raise HTTPException(status_code=409, detail="App already registered.")

    commit_changes_to_object(db, db_app)
    return db_app

def delete_app(db:Session, app:App, app_id:str):
    """To delete an app entry"""
    query=db.query(App).filter(app.app_id==app_id)
    if query is None:
   	    raise HTTPException(status_code=409, detail="App not found.")
    db.delete(query)
    commit_changes_to_object(db, query)

def update_app(db:Session, app:App, update_app:updateApp, app_id:str):
    """To update the app profile"""
    query=db.query(App).filter(app.app_id== app_id)
    if query is None:
         raise HTTPException(status_code=409, detail="App not found.")
    for name,entry in vars(app.dict(exclude_none=True)):
        db.execute(update(query.entry).values(updateApp.entry))
    commit_changes_to_object(db, query)
    return query

def get_apps(db: Session, app_id: str, user_id: str, name: str, app_name:str, limit = None, identify_by: dict = dict, offset: int = 0, 
sort_by: str = "user_id", order: str = "asc"):
    """Displays all the app profiles"""
    query = db.query(App).filter_by(**identify_by).offset(offset).limit(limit).\
        order_by("%s %s" % (sort_by, order))
    total = db.query(func.count(App.app_id)).scalar()
    
    if user_id:
        return db.query(App).filter(App.user_id == user_id).all()
    
    if name:
        return db.query(App).filter(App.name == name).all()
    
    if app_id:
        return db.query(App).filter(App.app_id == app_id).all()
    
    if app_name:
        return db.query(App).filter(App.app_name == app_name).all()
    return [{'Total number of rows ': total}, query.all()]


