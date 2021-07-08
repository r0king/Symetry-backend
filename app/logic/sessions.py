from app.dbops.common import hash_string
import datetime

def make_session(user):
    return hash_string(user.email, user.id, datetime.datetime.utcnow().timestamp())
