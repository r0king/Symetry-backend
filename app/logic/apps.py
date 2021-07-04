from datetime import timedelta
from app.dbops.common import hash_string
from app.schemas.tokens import TokenCreate
from app.dbops.tokens import create_token, get_token_by_id, list_tokens
from app.exceptions import IntendedException
from app.dbops.apps import create_app, get_app_by_id, get_app_by_name
from app.schemas.apps import App
from jose import JWTError, jwt

def create_app_endpoint(database, app: App):
    """
    Logic to create app
    """
    conflicted_app = get_app_by_name(
        database,
        name=app.name
    )

    if getattr(conflicted_app, "name") == app.name:
        raise IntendedException("App with same name exists", 409)

    return create_app(database, app)


def check_token_id_exists(database, token_id: int ):
    """
    Check app    
    """
    # validate the token_id

    token = get_token_by_id(database,token_id=token_id)

    if not token:
        raise IntendedException("Token doesn't exists", 404)

    return token
    


def app_login_endpoint(database, token:TokenCreate):
    """
    create and return token    
    """
    try:
        tokenrow = create_token(database,token)
        app = get_app_by_id(database,token.app_id)
    except:
        raise IntendedException('Internal Server Error',status_code=500)

    #set time to expire        
    tokenrow.timestamp += timedelta(minutes=120)

    #create the token 
    Secret = hash_string(tokenrow.user_id)+'|'+hash_string(app.id)+'|'+hash_string(app.secret)
    jwt_token =  jwt.encode(hash_string(tokenrow.timestamp),Secret,algorithm='HS256')

    return jwt_token
    
