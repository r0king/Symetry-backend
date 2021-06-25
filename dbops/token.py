

from sqlalchemy.orm.session import Session
from database import models, datamodels


def get_Token( db: Session, id: int):
     return db.query(models.Token).filter(models.Token.id == id).first()

def get_user_id(db: Session, skip: int = 0, limit: int = None, identify_by=dict , sort_by="id", sort_order="asc"):
    if limit is None:
        return db.query(models.Token).filter_by(**identify_by).offset(skip).order_by("%s %s" % (sort_by, sort_order)).all()

    return db.query(models.Token).filter_by(**identify_by).offset(skip).limit(limit).order_by("%s %s" % (sort_by, sort_order)).all()

def update_Token(ddb: Session, user_id,user_update_data:datamodels.UserUpdate ):
    query=db.query(models.Tokenr).filter_by(user_id= user_id).first()
    for var, value in vars(user_update_data).items():
        if value:
            setattr(query, var, value)
    db.add(query)
    db.commit()
    db.refresh(query)

    return query

    

    def create_Token(db: Session, Token: datamodels.CreateToken):
   
    db_Token= models.Token(**models.Token.dict())
    db.add(db_Token)
    db.commit()
    db.refresh(db_Token)
    
    return db_Token

def delete_Token(user_id , db: Session):
    query=db.query(models.Token).filter_by(user_id= user_id).first()
    query.is_active=False
    db.add(query)
    db.commit()
    db.refresh(query)




