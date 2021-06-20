"""
    User Table : User ID, Username, First Name, Last Name, Email, Password(Hashed), is_active, Contact, Roles etc. 

    Session Table : Session ID, User ID, Token ID etc
"""
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Session(Base):

    __tablename__ = 'session'

    user_id = Column(Integer, ForeignKey("user.id"))
    session_id = Column(String, unique=True, nullable=False)
    token_id = Column(String, unique=True, nullable=False)




""" 
    Logging : User ID, App ID, Time, Message

    App Table : App ID, App Secret(Hashed), App Name, Email, User ID (many to many)

    Token Table : User ID, App ID, Token ID
    
 """    
