"""
    GET / for root information on API. Return value.

    POST /user - registration . Return user details.

    GET /user - authentication. Return details of current user.

    POST /auth/login - create a new session. Return a token ID.

    POST /auth/logout - terminate a new session. 

    POST /app - registration. Return App ID and App Secret. 

    POST /access/validate - accept App Id, App Secret, User ID . Return Token ID

    POST /access/token - accept token Id from user. Return Token.

    GET /acess/token - for verification of token by 3rd party server. Returns True or False.

    GET /access/profile - verifies token. Return user details.

    GET /logging - keeps track of logging . Return logs. 


 """
