from hashlib import sha256
from app.dbops.logs import create_log
from datetime import timedelta
from app.dbops.common import hash_string
from app.schemas.tokens import TokenCreate
from app.dbops.tokens import create_token, get_token_by_id, list_tokens
from app.exceptions import IntendedException
from app.dbops.apps import create_app, get_app_by_id, get_app_by_user_id, list_apps
from app.schemas.apps import App, CreateApp
from jose import jwt
import time

def check_app(database, app_name: str, user_id: int):
    """
    check user has an app with same name
    """

    # check if user has an app with same app name

    user_apps = list_apps(database,
                          identify_by={
                              'user_id':user_id,
                              'name':app_name
                          })

    if user_apps:
        raise IntendedException("app with same name already exists",409)

def check_app_exists(database, app_id: str, user_id: int):
    """
    check user has an app with same name
    """

    # check if user has an app with same app name

    tokens = list_tokens(database,
                          identify_by={
                              'user_id':user_id,
                              'app_id':app_id
                          })

    if tokens:
        raise IntendedException("token for the app already exists",409)

def create_app_endpoint(database,app_name:str,current_user):
    """
    Logic to create app
    """
    secret = hash_string(current_user.id + app_name + )
    app = CreateApp(user_id=current_user.id,name=app_name,)
    return create_app(database,app)


def check_token_id_exists(database, token_id: int):
    """
    Check app    
    """
    # validate the token_id

    token = get_token_by_id(database, token_id=token_id)

    if not token:
        raise IntendedException("Token doesn't exists", 404)

    return token


def app_login_endpoint(database, app_id: int, user_id: int):
    """
    create and return token    
    """
    try:
        tokenrow = create_token(database, app_id, user_id)
        app = get_app_by_id(database, app_id)
    except Exception as e:
        create_log(user_id='32')
        raise IntendedException('Internal Server Error', status_code=500)

    # set time to expire
    tokenrow.timestamp += timedelta(minutes=120)

    # create the token
    Secret = hash_string(tokenrow.user_id)+'|' + \
        hash_string(app.id)+'|'+hash_string(app.secret)
    jwt_token = jwt.encode(hash_string(
        tokenrow.timestamp), Secret, algorithm='HS256')

    return jwt_token
