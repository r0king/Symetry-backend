# endpoints are updated in the readme
import uuid
from fastapi import FastAPI
from fastapi.params import Depends
from starlette.responses import PlainTextResponse, Response
from app.schemas.tokens import TokenCreate
from app.dbops.tokens import create_token
from app.schemas.users import CreateUser, User, UserLogin, UserUpdate
from app.schemas.apps import App, UpdateApp
from app.dependancies import LoginForm, get_current_user, get_db, oauth2_scheme
from app.dbops.users import delete_user, get_user_by_email_or_username, update_user, get_user
from app.dbops.apps import update_app, delete_app
from app.dbops.sessions import create_session, delete_session
from app.logic.users import create_user_endpoint, verify_user_credentials
from app.logic.common import is_same_user_or_throw
from app.logic.apps import is_same_app_or_throw
from app.logic.tokens import verify_token
from app.database.models import Session
from app.exceptions import IntendedException
from app.database import models
from app.database.database import set_up_database
from app.schemas.apps import CreateApp
from app.logic.apps import create_app_endpoint
from app.schemas.tokens import VerifyToken
from app.schemas.sessions import SessionCreate
from app.logic.sessions import make_session

models.Base.metadata.create_all(bind=set_up_database())

app = FastAPI()

@app.exception_handler(IntendedException)
def handle_intended_exception(_, exc):
    """
    Handle all intended exceptions
    """
    return PlainTextResponse(exc.message, status_code=exc.status_code)

# GET        /                      Get root information about the APIreturn [details ]

@app.get('/')
def root():
    """
    GET /
    Root page
    """
    return {
        "name": "Symetry API",
        "description": "Symertry SSO general API",
        "version": "0.0.1",
        "origin": "Float Business Accelerator",
        "team": "Monsoon '21 Batch"
    }


@app.get("/me/", response_model=User)
def get_logged_in_user(user: User = Depends(get_current_user)):
    """
    GET /auth/me/
    Get Current User Info
    """
    return user


@app.post("/user/", response_model=User)
def create_user(user: CreateUser, database: Session = Depends(get_db)):
    """
    POST /auth/user/

    Create a new user
    """
    return create_user_endpoint(database, user)


@app.get("/user/{user_id}/", response_model=User)
def retreive_user(user_id: int, current_user: User = Depends(get_current_user)):
    """
    GET /auth/user/:user_id
    Retreive user info by id
    """
    is_same_user_or_throw(current_user, user_id)
    return current_user


@app.patch("/user/{user_id}/", response_model=User)
def patch_user(
    user_id: int,
    updated_data: UserUpdate,
    database: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    PATCH /auth/user/:user_id
    Update user
    """
    is_same_user_or_throw(current_user, user_id)
    return update_user(database, user_id, updated_data)


@app.delete("/user/{user_id}/", response_model=User)
def destroy_user(
    user_id: int,
    database: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    DELETE /auth/user/:user_id
    Delete User
    """
    is_same_user_or_throw(current_user, user_id)
    return delete_user(database, user_id)


@app.post("/auth/login/")
def login_to_symetry(
    response: Response,
    credentials: LoginForm = Depends(),
    database: Session = Depends(get_db)
):
    """
    Login to symetry
    POST /auth/login/
    """
    this_user = get_user_by_email_or_username(database, username=credentials.username)
    if this_user and verify_user_credentials(this_user, credentials.password):
        new_session = SessionCreate(
            user_id=this_user.id,
            token=make_session(this_user),
            save_session=True
        )
        token_raw = new_session.token
        create_session(database, new_session)
        response.set_cookie(key="session", value=token_raw)
        # For swagger/openapi
        return {"access_token": token_raw, "token_type": "bearer"}
    raise IntendedException("Unauthenticated", 401)


@app.post("/token/check/")
def check(token_data: VerifyToken, database: Session = Depends(get_db)):
    """
    To check if given token is valid
    POST /token/check/
    """
    return verify_token(database, token_data)


@app.post("/auth/logout/", status_code=204)
def logout(
    database: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    delete session and logout.
    """
    if delete_session(database, token=token) is None:
        raise IntendedException("Session not found", 400)


@app.post("/app/", response_model=App)
def create_app(
    third_party_app: CreateApp,
    database: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    POST /app/
    Create a new third party app
    """
    return create_app_endpoint(database, third_party_app, current_user)


@app.post("/app/{app_id}/login/")
def login_to_app(
    app_id: uuid.UUID,
    database: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Login to app
    POST /app/:app_id/login/
    RETURNS TOKEN_ID
    """
    return create_token(
        database=database,
        token_data=TokenCreate(user_id=current_user.id, app_id=app_id)
    ).id


@app.patch("/app/{app_id}/", response_model=App)
def patch_app(
    app_id: uuid.UUID,
    updated_info: UpdateApp,
    database: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    PATCH /app/{app_id}/
    Update App
    """
    is_same_app_or_throw(database, app_id, current_user)
    return update_app(database, app_id, updated_info)


@app.delete("/app/{app_id}/", status_code=204)
def destroy_app(
    app_id: uuid.UUID,
    database: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    DELETE /app/{app_id}/
    Delete App
    """
    is_same_app_or_throw(database, app_id, current_user.id)
    delete_app(database, app_id)


# GET        /log/                  Gets the logs updated till then[List[log]] AUTHENTICATED

# Throw 403, if user has doesn't have permissions
# return logs from database
