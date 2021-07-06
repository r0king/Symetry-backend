# endpoints are updated in the readme
from app.schemas.tokens import TokenCreate
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from app.schemas.users import CreateUser, User, UserUpdate
from app.dependancies import get_current_user, get_db
from app.dbops.users import delete_user, update_user
from app.logic.users import create_user_endpoint
from app.logic.common import is_same_user_or_throw
from app.database.models import App, Session
from app.exceptions import IntendedException
from app.database import models
from app.database.database import set_up_database
import app.schemas.apps as appSchemas
from app.logic.apps import app_login_endpoint, check_app, check_token, create_app_endpoint
models.Base.metadata.create_all(bind=set_up_database())

app = FastAPI()


@app.exception_handler(IntendedException)
def handle_intended_exception(_, exc):
    """
    Handle all intended exceptions
    """
    raise HTTPException(detail=exc.message, status_code=exc.status_code)

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

# GET        /auth/me/            Get Current User Info[user] AUTHENTICATED

# Retrieve row from database
# Return user


@app.get("/auth/me/", response_model=User)
def get_logged_in_user(user: User = Depends(get_current_user)):
    """
    GET /auth/me/
    Get Current User Info
    """
    return user

# POST       /auth/user/            Create a new User (Registration)[user ]

# Validate
# Throw if email or username is duplicate
# Create user in database
# Return new user


@app.post("/auth/user/", response_model=User)
def create_user(user: CreateUser, database: Session = Depends(get_db)):
    """
    POST /auth/user/

    Create a new user
    """
    return create_user_endpoint(database, user)

# GET       /auth/user/{user_id}/       Get User By ID[user] AUTHENTICATED

# Throw 403, if user has doesn't have permissions
# Throw 404, if user with user_id doesn't exist in database
# Retrieve row from database
# Return user


@app.get("/auth/user/{user_id}", response_model=User)
def retreive_user(user_id: int, current_user: User = Depends(get_current_user)):
    """
    GET /auth/user/:user_id
    Retreive user info by id
    """
    is_same_user_or_throw(current_user, user_id)
    return current_user


# PATCH      /auth/user/{user_id}/  Update Existing User Info[user] AUTHENTICATED

# Validate
# Throw 403, if user has doesn't have permissions
# Throw 404, if user with user_id doesn't exist in database
# Update User's data in database
# Return updated user

@app.patch("/auth/user/{user_id}", response_model=User)
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

# DELETE     /auth/user/{user_id}/  Soft Delete User by ID[user] AUTHENTICATED

# Throw 403, if user has doesn't have permissions
# Throw 404, if user with user_id doesn't exist in database
# Soft delete user
# Return deleted user


@app.delete("/auth/user/{user_id}", response_model=User)
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

# POST       /auth/login/           Return tokenID by submitting credentials return ["token_id": STRING  ]

# POST       /auth/validate/        Creates a session by submitting tokenIDreturn [{"token": STRING, "type": STRING}  ]

# POST       /auth/check/           Checks if a token is validreturn ["status": BOOLEAN  ]

# POST       /auth/logout/          Terminates the sessionreturn [loged out sussesfully ]

# POST       /app              Create a new App (Registration)return [app  ]
# Validate user
# Authorise user
# Throw 409 , if same app exists for user
# Create and store time
# Create app in database
# Return new app with app_id


@app.post("/app", response_model=appSchemas.App)
def create_app(
    app_name: str,
    database: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """

     POST /app
     Create a new third party app

     """

    # checks user has app with same name
    check_app(database, app_name, current_user.id)
    return create_app_endpoint(database, app_name=app_name,  user_id=current_user.id)

# POST       /app/{app_id}/login/       Creates a session by submitting credentials return ["token": STRING  ]
# Validate app_id
# Throw 404, if app-id doesn't exist
# create a token in database(table)
# Return token_id


@app.post(" /app/{app_id}/login", response_model=App)
def create_app_session(
    app_id: int,
    database: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """

    POST /app/:app_id/login
    validate and return token

    """
    # check if the user is the owner of app ( search by app_id )
    app_name = check_token(database, app_id, current_user.id)

    # return token id
    return app_login_endpoint(database, app_name=app_name, app_id=app_id, user_id=current_user.id)


# PATCH      /auth/app/{app_id}/    Update Existing App Inforeturn [app]

# DELETE     /auth/app/{app_id}/    Soft Delete App by IDreturn [app]

# GET        /log/                  Gets the logs updated till then[List[log]] AUTHENTICATED

# Throw 403, if user has doesn't have permissions
# return logs from database
