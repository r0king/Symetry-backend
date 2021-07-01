"""

"""
from app.exceptions import IntendedException
from app.schemas.users import CreateUser
from app.dbops.users import create_user, get_user_by_email_or_username


def create_user_endpoint(database, user: CreateUser):
    """
    Logic for create user endpoint
    """
    conflicted_user = get_user_by_email_or_username(
        database,
        username=user.username,
        email=user.email
    )

    if getattr(conflicted_user, "email") == user.email:
        raise IntendedException("Email is not unique")
    if getattr(conflicted_user, "username") == user.username:
        raise IntendedException("Username is not unique")

    return create_user(database, user)
