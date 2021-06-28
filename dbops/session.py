from sqlalchemy.orm import Session
from sqlalchemy import func
from dbops.common import commit_changes_to_object
from database.models import Session as SessionTable
from database.datamodels import SessionCreate
from hashlib import sha256

def list_sessions(
    db: Session,
    identify_by: dict = dict,
    offset: int = 0,
    limit=None,
    order: str = "desc",
    sort_by: str = "timestamp"
):                      # get all sessions
    query = db.query(SessionTable)\
        .filter_by(**identify_by)\
        .offset(offset).\
        order_by("%s %s" % (sort_by, order))

    
    # count = db.execute(
    #                 # db
    #                 #     .query(SessionTable).filter_by(**identify_by).offset(offset)
    #                 #     .order_by("%s %s" % (sort_by, order))
    #                     query.statement.with_only_columns([func.count()])
    #                 ).scalar()

    count = db.query(func.count('*'))\
        .select_from(SessionTable)\
        .filter_by(**identify_by)\
        .offset(offset).\
        order_by("%s %s" % (sort_by, order))
        
    if limit:
        return [
            {'Session count': count.scalar()},
            query.limit(limit).all()
        ]

    return [
        {'Session count': count.scalar()},
        query.all()]


def get_session_by_id(
        db: Session,
        id:  int):        # get session id

    return db.query(SessionTable).filter_by(id=id).first()


def delete_session(
        db: Session,
        id: int):
    # delete session
    query = db.query(SessionTable).filter_by(id=id).first()
    db.delete(query)
    db.commit()

    return query


def create_session(
        database: Session,
        token:str,
        session: SessionCreate):

    user_session = SessionTable(
            **session.dict(),
            hashed_token =sha256(token),    #save hashed token

    )
    commit_changes_to_object(database, user_session)

    return token            #return user unhashed token
