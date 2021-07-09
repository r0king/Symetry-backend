# symetry--backend

Backend API Server 

- FastAPI
- SQLAlchemy
- Sqlite

## Setting up Dev 

```
git clone  <repoID>
cd symetry

# Without Docker
virtualenv env
source env/bin/activate
pip install -r requirements.txt

# With docker(and compose)
docker-compose up -d
```

### Environment Variables

| NAME | DESC | TYPE | DEFAULT | REQUIRED |
| --- | --- | --- | --- | --- |
| DATABASE_URL | The database url | Url String | - | YES |

### JSON Schema

#### Create User
```
{
  "username": STRING
  "name": STRING,
  "email": STRING,
  "password": STRING,
  "contact": STRING,[OPTIONAL]
}
```
#### Receive User
```
{
  "username": STRING,
  "email": STRING, 
  "name": STRING, 
  "contact": STRING,
  "id": INTEGER, 
}
```
#### Update User
```
{
  "username": STRING[OPTIONAL],
  "name": STRING[OPTIONAL],
  "email": STRING[OPTIONAL],
  "password": STRING[OPTIONAL],
  "contact": STRING[OPTIONAL],
}
```
#### Create App
```
{
  "name": STRING,
  "email": STRING,
  "password": STRING,
  "contact": STRING
}
```
#### Receive App
```
{
  "name": STRING,
  "email": STRING,
  "password": STRING,
  "contact": STRING,
  "app_id": STRING,
  "app_secret": STRING
}
```
#### Update App
```
{
  "name": STRING[OPTIONAL],
  "email": STRING[OPTIONAL],
  "password": STRING[OPTIONAL],
  "contact": STRING[OPTIONAL]
}
```
#### User Login 
```
{
  "username": STRING, 
  "password": STRING,
  "app_id": STRING,
}
```
#### Logs
```
{
  "user": STRING,
  "app": STRING,
  "time": TIME,
  "message": STRING
}
```

### Endpoints

| URL | DESCRIPTION | METHOD | PARAMS | AUTHENTICATED | RESPONSE |
| --- | --- | --- | --- | --- | --- |
| `/` | Get root information about the API | GET | - | No | - |
| `/auth/user/` | Get Current User Info | GET | - | Yes | [User](#receive-user) |
| `/auth/user/` | Create a new User (Registration) | POST | [User](#create-user) | No | [User](#receive-user) |
| `/auth/user/{user_id}/` | Update Existing User Info | PATCH | [UserUpdate](#update-user) | Yes |  [User](#receive-user) |
| `/auth/user/{user_id}/` | Soft Delete User by ID | DELETE | - | Yes |  - |
| `/auth/login/` | Return tokenID by submitting credentials | POST | [UserLogin](#user-login) | Yes | `"token_id": STRING` |
| `/auth/validate/` | Creates a session by submitting tokenID | POST | `"token_id": STRING` | No | `{"token": STRING, "type": STRING}` |
| `/auth/check/` | Checks if a token is valid | POST | `"token": STRING` | Yes | `"status": BOOLEAN` |
| `/auth/logout/` | Terminates the session | POST | - | Yes | - |
| `/auth/app` | Create a new App (Registration) | POST | [App](#create-app) | No | [App](#receive-app) |
| `/auth/app/login/` | Creates a session by submitting credentials | POST | [AppLogin](#app-login) | Yes | `"token": STRING` |
| `/auth/app/{app_id}/` | Update Existing App Info | PATCH | [AppUpdate](#update-app) | Yes |  [App](#receive-app) |
| `/auth/app/{app_id}/` | Soft Delete App by ID | DELETE | - | Yes |  - |
| `/log/` | Gets the logs updated till then | GET | - | Yes | `` |


Tasks will be assigned as "Issues" Check the project board. 

### Tokens

Token contains 3 parts before encoding with base64(UTF-8)

- hashed -> SHA256 Hash of app_id, app_secret, user_id and datetime
- user_id
- datetime

This is stored as a json string and then encoded into base64(UTF-8)

For verification from app's perspective

- Decode the token using base64(UTF-8)
- Load the json string and obtain user_id and datetime
- Use your app_id and the SHA256 hash of your app_secret along with user_id and datetime from token and hash it with SHA256.
- Compare the hashed part of the token with the hash you've obtained, for valid tokens it should match

