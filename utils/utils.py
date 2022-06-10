import asyncio
import logging

from bson import ObjectId
from fastapi import HTTPException
from starlette import status
import os

import service.chat
from exceptions.chat_exceptions import ChatNotFound
from models.chat import ChatModel

logger = logging.getLogger('main-logger')


def verify_api_key(api_key):
    backoffice_app_api_key = os.getenv('BACKOFFICE_API_KEY')
    native_app_api_key = os.getenv('NATIVE_APP_API_KEY')
    if os.getenv("CURRENT_ENVIRONMENT") == "production" and api_key not in [backoffice_app_api_key, native_app_api_key]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Api key not valid")


def log_request_body(request_id, body):
    asyncio.ensure_future(_log_request_body(request_id, body))


async def _log_request_body(request_id, body):
    logger.info(f"Request: {request_id} - Body: {body}")


def check_valid_chat_id(chat_id):
    if not ObjectId.is_valid(chat_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Chat ID '{chat_id}' is not valid")
    return chat_id


def validate_chat(chat_id: str):
    check_valid_chat_id(chat_id)
    chat = service.chat.get(chat_id)
    if not chat:
        raise ChatNotFound(chat_id)
    return chat_id
