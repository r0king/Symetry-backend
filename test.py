from app.database import models
from app.database.database import set_up_database
from app.database.config_db import SessionLocal

models.Base.metadata.create_all(bind=set_up_database())

# This database variable can be passed to dbops functions.
database = SessionLocal()