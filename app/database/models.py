"""
Database Models
"""
import uuid
# For postgres
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean, Integer, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import UniqueConstraint
from app.database.config_db import Base


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
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class Session(Base):
    """
    SESSIONS MODEL
    sessionID, tokenID and a one to one relation with the user
    this is for the user to log into our program only.
    no session data of the 3rd party apps are stored here.

    A= Sha(username+TOKEN-ID+hashedpassword+SECRET)
    ->store into Sha(A) Sessions table.

    """
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    save_session = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

class Logging(Base):
    """
    LOGGING MODEL
    User ID, App ID, Time, Message
    """
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"))
    timestamp = Column(DateTime, server_default=func.now())
    message = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

class Token(Base):
    """
     TOKEN MODEL
     User ID, App ID, Token ID
    """
    __tablename__ = "tokens"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # Generate UUID
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"))
    timestamp = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

class App(Base):
    """
    APP MODEL
    App ID, App Secret(Hashed), App Name, Email, Password(Hashed), User ID (many to many)
    """
    __tablename__ = "apps"
    # Make user_id and app_name unique together
    __table_args__ = tuple(UniqueConstraint("user_id", "name", name="user_app_name"))

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    secret = Column(String, nullable=False)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
