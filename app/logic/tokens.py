"""
Token utils
"""
import json
import base64
from datetime import datetime
from app.schemas.tokens import VerifyToken
from app.dbops.apps import get_app_by_id
from app.dbops.common import hash_string


def get_token_hash(third_party_app, user_id, timestamp):
    """
    Hash token according to a certain order
    """
    print(third_party_app.id, third_party_app.secret, user_id, timestamp)
    return hash_string(third_party_app.id, third_party_app.secret, user_id, timestamp)


def make_token(third_party_app, user_id, timestamp: datetime):
    """
    Create Token for apps
    """
    token_data = {
        "token": get_token_hash(third_party_app, user_id, timestamp.timestamp()),
        "user_id": user_id,
        "timestamp": timestamp.timestamp()
    }
    return base64.b64encode(json.dumps(token_data).encode("utf-8"))


def verify_token(database, token_data: VerifyToken):
    """
    Recreate and verify token
    """
    json_str = base64.b64decode(token_data.token).decode("utf-8")
    token_obj = json.loads(json_str)
    app = get_app_by_id(database, token_data.app_id)
    hashed_val = get_token_hash(app, token_obj["user_id"], token_obj["timestamp"])
    return hashed_val == token_obj["token"]
