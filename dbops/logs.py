"""
Database opertaions for Logging class
"""
from sqlalchemy.orm import Session
from dbops.common import commit_changes_to_object, list_table
from database.models import Logging
from schemas.logs import CreateLog


def list_logs(database: Session, **kwargs):
    """
    List logs

    Same Params as for common.list_table
    """
    return list_table(database, Logging, **kwargs)


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
