from app.exceptions import IntendedException


def is_same_user_or_throw(auth_user, user_id):
    """
    Check if authenticated user's id matches route parameter
    """
    if auth_user.id != user_id:
        raise IntendedException("User doesn\'t have permission to access this resource", 403)


def is_same_app_or_throw(auth_app, app_id):
    """
    Check if authenticated app's id matches route parameter
    """
    if auth_app.id != app_id:
        raise IntendedException("User doesn\'t have permission to access this resource", 403)