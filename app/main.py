# endpoints are updated in the readme
from fastapi import FastAPI
from fastapi.params import Depends
from starlette.responses import PlainTextResponse
from app.schemas.tokens import TokenCreate
from app.dbops.tokens import create_token
from app.schemas.users import CreateUser, User, UserUpdate
from app.schemas.apps import App, UpdateApp
from app.dependancies import get_current_user, get_db
from app.dbops.users import delete_user, update_user
from app.dbops.apps import update_app, delete_app
from app.logic.users import create_user_endpoint
from app.logic.common import is_same_user_or_throw
from app.logic.apps import is_same_app_or_throw
from app.database.models import Session
from app.exceptions import IntendedException
from app.database import models
from app.database.database import set_up_database
import app.schemas.apps as appSchemas
from app.logic.apps import create_app_endpoint

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

# GET        /auth/me/            Get Current User Info[user] AUTHENTICATED

# Retrieve row from database
# Return user

@app.get("/me/", response_model=User)
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

@app.post("/user/", response_model=User)
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

@app.get("/user/{user_id}/", response_model=User)
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

# DELETE     /auth/user/{user_id}/  Soft Delete User by ID[user] AUTHENTICATED

# Throw 403, if user has doesn't have permissions
# Throw 404, if user with user_id doesn't exist in database
# Soft delete user
# Return deleted user

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

# POST       /auth/login/           Return tokenID by submitting credentialsreturn ["token_id": STRING  ]
#Enter credentials
#Throw error 400, if login credentials are invalid.
#Return TokenID

# POST       /auth/validate/        Creates a session by submitting tokenID return [{"token": STRING, "type": STRING}  ]
#submit tokenID
#Throw 409 error, if session expires. 
#return Token and Type


# POST       /auth/check/           Checks if a token is validreturn ["status": BOOLEAN  ]

# Throw 401 , if token is invalid.
#return status true or false

# POST       /auth/logout/          Terminates the sessionreturn [loged out sussesfully ]
# Delete session

# delete session 
# return logged out successfully.

# POST       /auth/app              Create a new App (Registration)return [app  ]
# Validate user
# Throw 409 , if app exists
# Create app in database
# Return new app with app_id

@app.post("/app/", response_model=appSchemas.App)
def create_app(
    third_party_app: appSchemas.CreateApp,
    database: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    POST /app/
    Create a new third party app
    """
    return create_app_endpoint(database, third_party_app, current_user)

# POST       /auth/app/{app_id}/login/       Creates a session by submitting credentials return ["token": STRING  ]
# Throw 404, if app-id or user_id doesn't exist
# create token eg:['user_id+app_id+randomvalue',token_id,'app_secret+timestamp']
# Hash and store token
# Return token

@app.post("/app/{app_id}/login/")
def login_to_app(
    app_id: int,
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

# PATCH      /auth/app/{app_id}/    Update Existing App Inforeturn [app]
# Validate
# Throw 403, if user has doesn't have permission
# Update App name in database
# Return updated user

@app.patch("/app/{app_id}/", response_model=App)
def patch_app(
    app_id: int,
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


# DELETE     /auth/app/{app_id}/    Soft Delete App by IDreturn [app]
# Validate
# Throw 403, if user has doesn't have permissions
# Soft delete app
# Return deleted app

@app.delete("/app/{app_id}/", status_code=204)
def destroy_app(
    app_id: int,
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
