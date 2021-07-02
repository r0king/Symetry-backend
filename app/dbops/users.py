"""
CRUD Operations on users table
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.dbops.common import commit_changes_to_object, hash_string, list_table
from app.database import models
from app.schemas.users import CreateUser, UserUpdate


def get_user(database: Session, user_id: int):
    """
    Get User By Primary Key
    """
    return database.query(models.User).filter_by(is_active=True, id=user_id).first()


def get_user_by_email_or_username(database: Session, email: str = None, username: str = None):
    """
    Get User By Unique Email Or Username
    """
    return database.query(models.User).filter(
        (models.User.email == email) | (models.User.username == username)
    ).first()


def list_users(database: Session, **kwargs):
    """
    List users

    Same Params as for common.list_table
    """
    return list_table(database, models.User, **kwargs)


def update_user(database: Session, user_id: int, user_update_data: UserUpdate):
    """
    Update User
    """
    db_user = get_user(database, user_id)

    if user_update_data.password is not None:
        user_update_data.password = hash_string(user_update_data.password)

    for var, value in vars(user_update_data).items():
        if value:
            setattr(db_user, var, value)

    commit_changes_to_object(database, db_user)

    return db_user


def create_user(database: Session, user: CreateUser):
    """
    Create User in Database
    """
    user.password = hash_string(user.password)
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
