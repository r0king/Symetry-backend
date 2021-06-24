from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from dbops.common import commit_changes_to_object
from database.models import App
from database.datamodels import CreateApp

def create_app(db:Session, app:CreateApp):
    "To create a new entry"
    db_app=App(user_id=app.user_id, password=app.password, email=app.email, contact=app.contact,app_name=app.app_name)

    if db_app:
   	    raise HTTPException(status_code=409, detail="App already registered.")

    commit_changes_to_object(db, db_app)
    return db_app

def delete_app(db:Session, app:App, user_id:int):
    "To delete an app entry"
    query=db.query(App).filter_by(app.user_id==user_id)
    if query:
   	    raise HTTPException(status_code=409, detail="App not found.")
    db.delete(query)
    db.commit()
def update_app(db:Session, app:App, user_id:int):
     query=db.query(App).filter_by(app.user_id== user_id)
     if query:
   	    raise HTTPException(status_code=409, detail="App not found.")
    
def get_all_apps()
