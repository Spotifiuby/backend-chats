import datetime
from config.db import conn


def _token_entity(token) -> dict:
    if not token:
        return token
    token['id'] = str(token.pop('_id'))
    return token


def get_token(user_id):
    token = conn.tokens.find_one({'user_id': user_id})
    return _token_entity(token)


def create(user_id, token):
    conn.tokens.delete_many({'user_id': user_id})
    token_dict = {
        'user_id': user_id,
        'token': token,
        'date_created': datetime.datetime.today()
    }
    r = conn.tokens.insert_one(token_dict)
    mongo_token = conn.tokens.find_one({"_id": r.inserted_id})

    return _token_entity(mongo_token)
