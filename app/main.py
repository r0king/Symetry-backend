# endpoints are updated in the readme
from fastapi import FastAPI


# GET        /                      Get root information about the APIreturn [details ]
# GET        /auth/user/            Get Current User Inforeturn [user ]
# POST       /auth/user/            Create a new User (Registration)return [user ]
# PATCH      /auth/user/{user_id}/  Update Existing User Inforeturn [user  ]
# DELETE     /auth/user/{user_id}/  Soft Delete User by IDreturn [user  ]
# POST       /auth/login/           Return tokenID by submitting credentialsreturn ["token_id": STRING  ]
# POST       /auth/validate/        Creates a session by submitting tokenIDreturn [{"token": STRING, "type": STRING}  ]
# POST       /auth/check/           Checks if a token is validreturn ["status": BOOLEAN  ]
# POST       /auth/logout/          Terminates the sessionreturn [loged out sussesfully ]
# POST       /auth/app              Create a new App (Registration)return [app  ]
# POST       /auth/app/login/       Creates a session by submitting credentialsreturn ["token": STRING  ]
# PATCH      /auth/app/{app_id}/    Update Existing App Inforeturn [app ]
# DELETE     /auth/app/{app_id}/    Soft Delete App by IDreturn [app ]
# GET        /log/                  Gets the logs updated till thenreturn [log ]

app = FastAPI()


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

from .test import test
