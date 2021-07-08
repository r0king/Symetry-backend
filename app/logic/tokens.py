"""

"""
from app.schemas.tokens import VerifyToken
import json
import base64
from app.dbops.apps import get_app_by_id
from app.dbops.common import hash_string


def get_token_hash(third_party_app, user_id, timestamp):
    return hash_string(third_party_app.id, third_party_app.secret, user_id, timestamp)


def create_token(third_party_app, user_id, timestamp):
    """
    Create Token for apps
    """
    token_data = {
        "token": get_token_hash(third_party_app, user_id, timestamp),
        "user_id": user_id,
        "timestamp": timestamp
    }
    return base64.b64encode(json.dumps(token_data).encode("utf-8"))


def verify_token(database, token_data: VerifyToken):
    """
    Recreate and verify token
    """
    json_str = base64.b85decode(token_data.token).decode("utf-8")
    token_data = json.loads(json_str)
    app = get_app_by_id(database, token_data.app_id)
    hashed_val = get_token_hash(app, token_data["user_id"], token_data["timestamp"])
    return hashed_val == token_data["token"]
