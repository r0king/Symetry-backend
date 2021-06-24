from fastapi import FastAPI, HTTPException, applications
from sqlalchemy.orm import Session
from dbops.common import commit_changes_to_object
from database.models import App
from database.datamodels import CreateApp

def create_app(db:Session, app:CreateApp, ):
    """To create a new entry"""
    db_app=App(**app.dict())
    if db_app:
   	    raise HTTPException(status_code=409, detail="App already registered.")

    commit_changes_to_object(db, db_app)
    return db_app

def delete_app(db:Session, app:App, user_id:int):
    """To delete an app entry"""
    query=db.query(app).filter_by(app.user_id==user_id)
    if query:
   	    raise HTTPException(status_code=409, detail="App not found.")
    db.delete(query)
    db.commit()

def update_app(db:Session, app:App, user_id:int):
    """To update the app profile"""
    query=db.query(app).filter_by(app.user_id== user_id)
    if query:
   	    raise HTTPException(status_code=409, detail="App not found.")
    
def get_all_apps(db: Session, limit = None, identify_by: dict = dict,offset: int = 0, sort_by: str = "user_id", order: str = "asc"):
    """Displays all the app profiles"""
    query = db.query(App).filter_by(**identify_by).offset(offset).limit(limit).\
        order_by("%s %s" % (sort_by, order))
    return query.all()

def get_user(db: Session, user_id: int):
    """Search by user id"""
    return db.query(App).filter_by(App.user_id= user_id).all()

def get_user_by_name(db: Session, name: str):
    """Search by username"""
    return db.query(App).filter(App.name == name).first()

def get_user_by_email(db: Session, email: str):
    """Search by user email"""
    return db.query(App).filter(App.email == email).first()

def get_user_by_contact(db: Session, contact: str):
    """Search by user contact"""
    return db.query(App).filter(App.contact == contact).first()

def get_user_by_app_id(db: Session, app_id: str):
    """Search by app id"""
    return db.query(App).filter(App.app_id == app_id).first()

def get_user_by_app_name(db: Session, app_name: str):
    """Search by app name"""
    return db.query(App).filter(App.app_name == app_name).first()








