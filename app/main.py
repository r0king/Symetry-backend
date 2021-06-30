# endpoints are updated in the readme
from fastapi import FastAPI



app = FastAPI()

# GET        /                      Get root information about the APIreturn [details ]

@app.get('/')
def root():
    detail = {
        "name": "Symetry API",
        "description": "Symertry SSO general API",
        "version": "0.0.1",
        "origin": "Float Business Accelerator",
        "team": "Monsoon '21 Batch"
    }

    return detail
# GET        /auth/me/            Get Current User Info[user] AUTHENTICATED

# Retrieve row from database
# Return user

# POST       /auth/user/            Create a new User (Registration)[user ]

# Validate
# Throw if email or username is duplicate
# Create user in database
# Return new user

# GET       /auth/user/{user_id}/       Get User By ID[user] AUTHENTICATED

# Throw 403, if user has doesn't have permissions
# Throw 404, if user with user_id doesn't exist in database
# Retrieve row from database
# Return user

# PATCH      /auth/user/{user_id}/  Update Existing User Info[user] AUTHENTICATED

# Validate
# Throw 403, if user has doesn't have permissions
# Throw 404, if user with user_id doesn't exist in database
# Update User's data in database
# Return updated user

# DELETE     /auth/user/{user_id}/  Soft Delete User by ID[user] AUTHENTICATED

# Throw 403, if user has doesn't have permissions
# Throw 404, if user with user_id doesn't exist in database
# Soft delete user
# Return deleted user

# POST       /auth/login/           Return tokenID by submitting credentialsreturn ["token_id": STRING  ]

# POST       /auth/validate/        Creates a session by submitting tokenIDreturn [{"token": STRING, "type": STRING}  ]

# POST       /auth/check/           Checks if a token is validreturn ["status": BOOLEAN  ]

# POST       /auth/logout/          Terminates the sessionreturn [loged out sussesfully ]

# POST       /auth/app              Create a new App (Registration)return [app  ]

# POST       /auth/app/login/       Creates a session by submitting credentialsreturn ["token": STRING  ]

# PATCH      /auth/app/{app_id}/    Update Existing App Inforeturn [app ]

# DELETE     /auth/app/{app_id}/    Soft Delete App by IDreturn [app ]

# GET        /log/                  Gets the logs updated till thenreturn [log ]
