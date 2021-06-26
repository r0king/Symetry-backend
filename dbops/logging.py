"""
Database opertaions for Logging class
"""
from sqlalchemy.orm import Session
from database.models import Logging
from dbops.common import commit_changes_to_object


def read_log_by_id(database: Session, log_id: int):
    """
    Read log by id
    """
    return database.query(Logging).filter(Logging.id == log_id).first()


def create_log(database: Session, log):
    """
    Create a log
    :param log: Must contain app_id, user_id and message
    TODO: Create Log's schemas
    """
    db_log = Logging(
        user_id = log.user_id,
        app_id = log.app_id,
        message = log.message
    )
    commit_changes_to_object(database, db_log)
