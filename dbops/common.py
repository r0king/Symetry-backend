"""
Common utilities for database operations
"""
from sqlalchemy.orm import Session
from database.config_db import Base


def commit_changes_to_object(database: Session, obj: Base):
    """Finish the database transaction and refresh session"""
    database.add(obj)
    database.commit()
    database.refresh(obj)


def list_table(
    database: Session,
    model,
    identify_by: dict=dict,
    offset: int=0,
    limit: int=None,
    order: str="desc",
    sort_by: str=None
):
    """
    List Tokens
    :param model: Pass the required model(as a class not object)
    :param limit: Limit the number of results
    :param identify_by: Dictionary of filters
    :param offset: Offset(Shift) the results by a certain value
    :param sort_by: Field to sort by
    :param order: asc for ascending, desc for descending
    """
    query = database.query(model).filter_by(**identify_by).offset(offset)

    if sort_by:
        query = query.order_by("%s %s" % (sort_by, order))

    if limit:
        return query.limit(limit).all()

    return query.all()
