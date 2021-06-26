"""
Database Models
"""
import datetime
from sqlalchemy import Column, String, Boolean, Integer, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.config_db import Base
from database.roles import Roles


class User(Base):
    """
    USER MODEL
    userID, username, name, email, password(Hashed), is_active, contact, roles,
    related to app
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    contact = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Roles), default=Roles.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
 


class Session(Base):
    """
    SESSIONS MODEL
    sessionID, tokenID and a one to one relation with the user
    """
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    token_id = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))


class Logging(Base):
    """
    LOGGING MODEL
    User ID, App ID, Time, Message
    """
    __tablename__ = "logs"


    user_id = Column(Integer, ForeignKey("users.id"))
    app_id = Column(String, ForeignKey("apps.id"))
    time = Column(DateTime, default=datetime.datetime.utcnow)
    message = Column(String)


class Token(Base):
    """
     TOKEN MODEL
     User ID, App ID, Token ID
    """
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    app_id = Column(String, ForeignKey("apps.id"))



class App(Base):
    """
    APP MODEL
    App ID, App Secret(Hashed), App Name, Password(Hashed), User ID (many to many)
    """
    __tablename__ = "apps"

    id = Column(String, primary_key=True)
    app_sec = Column(String, unique=True, nullable=False)
    app_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="app")
