"""
App logic
"""
from app.exceptions import IntendedException
from app.dbops.apps import get_app_by_id


def is_same_app_or_throw(database, app_id, current_user):
    """
    Check if logged in user is the owner of this app
    """
    app = get_app_by_id(database, app_id)
    if app.user_id != current_user.id:
        raise IntendedException("You don\'t have the appropriate timings", 403)
