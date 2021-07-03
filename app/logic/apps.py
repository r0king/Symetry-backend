from app.schemas.tokens import TokenCreate
from app.dbops.tokens import create_token, get_token_by_id, list_tokens
from app.exceptions import IntendedException
from app.dbops.apps import create_app, get_app_by_id, get_app_by_name
from app.schemas.apps import App


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


def check_token_id_exists(database, token: TokenCreate ):
    """
    Check app    
    """
    # check if app exists (user has created a token with the same app if then throw )
    # validate the token_id

    conflicted_token = list_tokens(
        database,
        identify_by={token.user_id: 'user_id',
                     token.app_id: 'app_id'   
                     }
    )

    if conflicted_token:
        raise IntendedException("Token already exists", 409)

    


def app_login_endpoint(database, token:TokenCreate):
    """
    create token    
    """
    # create and return token

    token = create_token(database,token)

    if token:
        return token
