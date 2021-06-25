from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user


from database import models, datamodels


def get_user(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = None, identify_by=dict , sort_by="id", sort_order="asc"):

    if limit is None:
        return db.query(models.User).filter_by(**identify_by).offset(skip).order_by("%s %s" % (sort_by, sort_order)).all()

    return db.query(models.User).filter_by(**identify_by).offset(skip).limit(limit).order_by("%s %s" % (sort_by, sort_order)).all()

def update_user(db: Session, user_id,user_update_data:datamodels.UserUpdate ):


    query=db.query(models.User).filter_by(user_id= user_id).first()
    for var, value in vars(user_update_data).items():
        if value:
            setattr(query, var, value)
    db.add(query)
    db.commit()
    db.refresh(query)

    return query




def create_user(db: Session, user: datamodels.CreateUser):
    user.password = user.password + "notreallyhashed"
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def delete_user(user_id , db: Session):
    query=db.query(models.User).filter_by(user_id= user_id).first()
    query.is_active=False
    db.add(query)
    db.commit()
    db.refresh(query)