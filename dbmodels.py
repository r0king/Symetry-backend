from sqlalchemy import Column, String, Boolean, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database.config_db import Base
from roles import Roles


class User(Base):
    """
    USER MODEL
    userID, username, first name, last name, email, password(Hashed), is_active, contact, roles,
    related to app
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    contact = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Roles), default=Roles.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    app_id = Column(Integer, ForeignKey("app.id"))

    app = relationship("User", back_populates="user")
