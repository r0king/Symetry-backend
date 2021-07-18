"""
App logic
"""
import sqlalchemy
from app.exceptions import IntendedException
from app.dbops.apps import get_app_by_id, create_app, list_apps
from app.schemas.apps import CreateApp


def is_same_app_or_throw(database, app_id, current_user):
    """
    Check if logged in user is the owner of this app
    """
    app = get_app_by_id(database, app_id)
    if app.user_id != current_user.id:
        raise IntendedException("You don\'t have the appropriate timings", 403)


def create_app_endpoint(database, app: CreateApp, current_user):
    """
    Logic to create app
    """
    try:
        return create_app(database, app, current_user.id)
    except sqlalchemy.exc.IntegrityError as unique_constraint_exception:
        raise IntendedException("", 409) from unique_constraint_exception


def list_apps_endpoint(database, current_user):
    """
    Logic to list user's apps
    """
    return list_apps(
        database,
        identify_by={'user_id':  current_user.id}
    )
