from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql.expression import desc
from dbops.common import commit_changes_to_object
from database.models import Session as SessionTable
from database.datamodels import SessionSchema


def list_sessions(
    db: Session,
    identify_by: dict = dict,
    offset: int = 0,
    limit=None,
    sort_by: str = "time",
    order: str = "desc"
):                      # get all sessions
    query = db.query(SessionTable).filter_by(**identify_by).offset(offset).\
        order_by("%s %s" % (sort_by, order))

    count = db.query(func.count(SessionTable.id)).scalar()

    if limit:
        return [
            {'Session count': count},
            query.limit(limit).all()
        ]

    return [
        {'Session count': count},
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
        session: SessionSchema):        # create session with user id

    user_session = SessionTable(**session.dict())
    commit_changes_to_object(database, user_session)

    return user_session
