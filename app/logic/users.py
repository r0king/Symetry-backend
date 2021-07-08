"""

"""
import sqlalchemy
from app.exceptions import IntendedException
from app.schemas.users import CreateUser
from app.dbops.users import create_user
from app.dbops.common import hash_string


def create_user_endpoint(database, user: CreateUser):
    """
    Logic for create user endpoint
    """
    try:
        return create_user(database, user)
    except sqlalchemy.exc.IntegrityError as unique_constraint_exception:
        raise IntendedException("Email/Username/Contact is not unique") from unique_constraint_exception


def verify_user_credentials(user, password):
    return user.password == hash_string(password)
