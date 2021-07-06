from sqlalchemy.sql.functions import func
from app.schemas.logs import CreateLog
from app.dbops.logs import create_log
from app.dbops.common import hash_string
from app.schemas.tokens import TokenCreate
from app.dbops.tokens import create_token
from app.exceptions import IntendedException
from app.dbops.apps import create_app, get_app_by_id, list_apps
from app.schemas.apps import CreateApp


def check_app(database, app_name: str, user_id: int):
    """
    check user has an app with same name
    """

    # check if user has an app with same app name

    user_apps = list_apps(database,
                          identify_by={
                              'user_id': user_id,
                              'name': app_name
                          })

    if user_apps:
        raise IntendedException("app with same name already exists", 409)


def create_app_endpoint(database, app_name: str, user_id: int):
    """
    Logic to create app
    """
    # create app secret
    secret = hash_string(app_name + func.now())+user_id
    # create app
    app_schema = CreateApp(user_id=user_id, name=app_name, secret=secret)
    app = create_app(database, app_schema)
    # create log
    log = CreateLog(
        message=f'[+] Created {app_name}', app_id=app.id, user_id=user_id)
    create_log(database, log)
    return app


def check_token(database, app_id: int, user_id: int):
    """
    Check app    
    """

    app = get_app_by_id(database, app_id=app_id)

    # check if the user is the owner of app (by app_id )

    if getattr(app, "app_id") != user_id:
        raise IntendedException("User not authorised to make the request", 401)

    return app.name


def app_login_endpoint(database, app_name: str, app_id: int, user_id: int):
    """
    create and return token    
    """

    try:
        # create the token
        token = TokenCreate(
            app_id=app_id,
            user_id=user_id,
            timestamp=func.now())
        tokenrow = create_token(database, token)
        
        log = CreateLog(
            message=f'[+] Created token for {app_name}',
            app_id=token.app_id,
            user_id=token.user_id)

    except Exception as e:
        log = CreateLog(
            message=f'[-] Error {e} Encoundered while creating token for {app_name}',
            app_id=app_id,
            user_id=user_id)
        raise IntendedException('Internal Server Error',
                                status_code=500)

    # create log
    create_log(database, log)

    # return token id
    return tokenrow.id
