import sqlalchemy
from app.exceptions import IntendedException
from app.dbops.apps import create_app
from app.schemas.apps import CreateApp

def create_app_endpoint(database, app: CreateApp, current_user):
    """
    Logic to create app
    """
    try:
        return create_app(database, app, current_user.id)
    except sqlalchemy.exc.IntegrityError as unique_constraint_exception:
        raise IntendedException("", 409) from unique_constraint_exception
