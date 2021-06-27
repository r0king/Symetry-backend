from fastapi import FastAPI, HTTPException, applications
from sqlalchemy.orm import Session, update
from dbops.common import commit_changes_to_object
from database.models import App
from database.datamodels import CreateApp,updateApp

def create_app(db:Session, app:CreateApp):
    """To create a new entry"""
    db_app=App(**app.dict())
    if db_app:
   	    raise HTTPException(status_code=409, detail="App already registered.")

    commit_changes_to_object(db, db_app)
    return db_app

def delete_app(db:Session, app:App, user_id:int):
    """To delete an app entry"""
    query=db.query(app).filter(app.user_id==user_id)
    if query:
   	    raise HTTPException(status_code=409, detail="App not found.")
    db.delete(query)
    commit_changes_to_object(db, query)

def update_app(db:Session, app:App, update_app:updateApp, user_id:int):
    """To update the app profile"""
    query=db.query(app).filter(app.user_id== user_id)
    if query is None:
        return None
    for name,entry in vars(app.dict()):
        db.execute(update(query.entry).values(updateApp.entry))
    commit_changes_to_object(db, query)
    return query
