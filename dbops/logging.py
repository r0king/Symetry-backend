"""
Database opertaions for Logging class
"""
from sqlalchemy.orm import Session
from dbops.common import commit_changes_to_object
from database.models import Logging
from database.datamodels import CreateLog


def get_all_logs(
    database: Session,
    limit = None,
    identify_by: dict = dict,
    offset: int = 0,
    sort_by: str = "time",
    order: str = "desc"
):
    """
    :param limit: Limit the number of results
    :param identify_by: Dictionary of filters
    :param offset: Offset(Shift) the results by a certain value
    :param sort_by: Field to sort by
    :param order: asc for ascending, desc for descending
    """

    # ** makes a dictionary into arguments
    # Eg: **{"a": b, "c": d} => a=b,c=d
    query = database.query(Logging).filter_by(**identify_by).offset(offset).\
        order_by("%s %s" % (sort_by, order))

    if limit:
        return query.limit(limit).all()
    return query.all()

def read_log_by_id(database: Session, log_id: int):
    """
    Read log by id
    """
    return database.query(Logging).filter(Logging.id == log_id).first()


def create_log(database: Session, log: CreateLog):
    """
    Create a log in DB
    """
    db_log = Logging(
        user_id = log.user_id,
        app_id = log.app_id,
        message = log.message
    )
    commit_changes_to_object(database, db_log)
    return db_log
