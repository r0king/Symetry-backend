# endpoints are updated in the readme
from fastapi.params import Depends
from sqlalchemy.orm import Session
from fastapi import FastAPI
from database.config_db import SessionLocal,Base
from dbops.session import list_sessions, create_session
from database.datamodels import SessionCreate
from database.database import set_up_database

app = FastAPI()

Base.metadata.create_all(bind=set_up_database)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET        /                      Get root information about the APIreturn [details ]


@app.post('/auth/create_session')
def new_session(usersession: SessionCreate, db: Session = Depends(get_db)):

    token = create_session(db, session=usersession, token='created token')

    return token


@app.get('/auth/create_session')
def get_sessions():
    detail = {
        "name": "Symetry API",
        "description": "Symertry SSO general API",
        "version": "0.0.1",
        "origin": "Float Business Accelerator",
        "team": "Monsoon '21 Batch"
    }

    return detail
