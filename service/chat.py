import datetime

from bson import ObjectId
import pymongo

from config.db import conn
from exceptions.chat_exceptions import ChatNotFound


def _chat_entity(chat) -> dict:
    if not chat:
        return chat
    chat['id'] = str(chat.pop('_id'))
    return chat


def get_chats(user_id):
    return [_chat_entity(chat) for chat in conn.chats.find({'users': user_id})]


def get(chat_id: str):
    chat = conn.chats.find_one({"_id": ObjectId(chat_id)})
    return _chat_entity(chat)


def create(user_id_1, user_id_2):
    chat_dict = {
        'users': [user_id_1, user_id_2],
        'messages': [],
        'date_created': datetime.datetime.today()
    }
    r = conn.chats.insert_one(chat_dict)
    mongo_chat = conn.chats.find_one({"_id": r.inserted_id})

    return _chat_entity(mongo_chat)


def is_owner(chat_id, user_id):
    chat = conn.chats.find_one({'_id': ObjectId(chat_id)})
    if not chat:
        raise ChatNotFound(chat_id)
    return user_id in chat['users']


def add_message(chat_id, user_id, text):
    message = {
        'sender': user_id,
        'text': text,
        'time': datetime.datetime.today()
    }
    updated_chat = conn.chats.find_one_and_update(
        {
            '_id': ObjectId(chat_id)
        }, {
            '$push': {
                'messages': message
            }
        },
        return_document=pymongo.ReturnDocument.AFTER
    )
    return _chat_entity(updated_chat)
