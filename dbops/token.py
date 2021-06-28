from sqlalchemy.orm import Token
from dbops.common import commit_changes_to_object
from database.models import Token
from database.datamodels import TokenSchema


def get_token_id(
        db: Token,
        Token: TokenSchema,app_id: int,user_id: int):  
              if(user_id)# get token id 
                return db.query(Token).filter_by(user_id == user_id)
              if(app_id)
                return db.query(Token).filter_by(app_id == app_id)
    return db.query(Token).filter(Token.user_id == session.user_id, Token.app_id == session.app_id).first()



def get_token_id_by_user_id(
        db:Token,
        user_id: int):                  # get token id with user id

    return db.query(Token).filter_by(user_id == user_id).first()


def create_token_id(
        db: Token,
        token: TokenSchema):        # create token with user id

    user_token = Token(**session.dict())
    commit_changes_to_object(database, token_id)

    return token_id
def delete_token(
        db: Token,
        token: TokenSchema):        # delete token id 

    query = db.query(Token).filter(Token.user_id == session.user_id, Token.app_id == session.app_id).first()
    db.delete(query)
    db.commit()
    db.refresh(query)
    return query
