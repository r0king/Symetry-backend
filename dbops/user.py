"""
CRUD Operations on users table
"""
from sqlalchemy.orm import Session
from dbops.common import commit_changes_to_object
from database import models
from schemas.users import CreateUser, UserUpdate


def get_user(database: Session, user_id: int):
    """
    Get User By Primary Key
    """
    return database.query(models.User).filter_by(is_active=True, id=user_id).first()


def get_user_by_email(database: Session, email: str):
    """
    Get User By Unique Email
    """
    return database.query(models.User).filter(models.User.email == email).first()


def get_users(database: Session,
    skip: int = 0,
    limit: int = None,
    identify_by=dict ,
    sort_by="id",
    sort_order="asc"
):
    """
    List Users
    :param database: Database Session
    :param skip: Offset value
    :param limit: No of records to be fetched, If None, fetches all records
    :param identify_by: Dictionary comtaining filters
    :param sort_by: sort by given field
    :param sort_order: sort either ascending(asc) or descending(desc)
    """
    if limit is None:
        return database.query(models.User).filter_by(is_active=True).filter_by(**identify_by).\
            offset(skip).order_by("%s %s" % (sort_by, sort_order)).all()

    return database.query(models.User).filter_by(is_active=True).filter_by(**identify_by).\
        offset(skip).limit(limit).order_by("%s %s" % (sort_by, sort_order)).all()


def update_user(database: Session, user_id: int, user_update_data: UserUpdate):
    """
    Update User
    """
    db_user = get_user(database, user_id)

    for var, value in vars(user_update_data).items():
        if value:
            setattr(db_user, var, value)

    commit_changes_to_object(database, db_user)

    return db_user


def create_user(database: Session, user: CreateUser):
    """
    Create User in Database
    """
    user.password = user.password + "notreallyhashed"
    db_user = models.User(**user.dict())
    commit_changes_to_object(database, db_user)

    return db_user


def delete_user(database: Session, user_id):
    """
    Soft delete user
    """
    db_user=get_user(database, user_id)
    db_user.is_active=False
    commit_changes_to_object(database, db_user)
