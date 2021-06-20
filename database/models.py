from sqlalchemy import Column, String, Boolean, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database.config_db import Base
from roles import Roles


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
    app_id = Column(Integer, ForeignKey("app.id"))

    app = relationship("App", back_populates="app")


class Session(Base):
    """
    SESSIONS TABLE
    sessionID, tokenID and a one to one relation with the user
    """
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    token_id = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
