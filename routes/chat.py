from fastapi import APIRouter, status, Header, Depends, Response
from typing import Optional

from utils.utils import log_request_body, check_valid_chat_id, verify_api_key
from models.chat import ChatModel, CreateChatRequest, AddMessageRequest
import service.chat
from exceptions.chat_exceptions import ChatNotFound, ChatNotOwnedByUser
from exceptions.user_exceptions import MissingUserId

chat_routes = APIRouter()


def _verify_user_id(user_id):
    if not user_id:
        raise MissingUserId()
    return user_id


def _verify_ownership(chat_id, user_id):
    if not service.chat.is_owner(chat_id, user_id):
        raise ChatNotOwnedByUser(chat_id, user_id)


@chat_routes.get('/chats', response_model=list[ChatModel], tags=['Chats'], status_code=status.HTTP_200_OK)
async def get_chats(response: Response,
                    q: Optional[str] = None,
                    x_user_id: Optional[str] = Header(None),
                    x_api_key: Optional[str] = Header(None),
                    authorization: Optional[str] = Header(None)):
    if authorization:
        response.headers['authorization'] = authorization
    verify_api_key(x_api_key)
    _verify_user_id(x_user_id)
    chats = service.chat.get_chats(x_user_id)
    return chats


@chat_routes.get('/chats/{chat_id}', response_model=ChatModel, tags=['Chats'], status_code=status.HTTP_200_OK)
async def get_chat(response: Response,
                   chat_id: str = Depends(check_valid_chat_id),
                   x_user_id: Optional[str] = Header(None),
                   x_api_key: Optional[str] = Header(None),
                   authorization: Optional[str] = Header(None)):
    if authorization:
        response.headers['authorization'] = authorization
    verify_api_key(x_api_key)
    _verify_user_id(x_user_id)
    _verify_ownership(chat_id, x_user_id)
    chat = service.chat.get(chat_id)
    if chat is None:
        raise ChatNotFound(chat_id)
    return chat


@chat_routes.post('/chats', response_model=ChatModel, tags=['Chats'], status_code=status.HTTP_201_CREATED)
async def create_chat(response: Response,
                      chat: CreateChatRequest,
                      x_user_id: Optional[str] = Header(None),
                      x_api_key: Optional[str] = Header(None),
                      authorization: Optional[str] = Header(None),
                      x_request_id: Optional[str] = Header(None)):
    if authorization:
        response.headers['authorization'] = authorization
    log_request_body(x_request_id, chat)
    verify_api_key(x_api_key)
    _verify_user_id(x_user_id)
    return service.chat.create(x_user_id, chat.user)


@chat_routes.put('/chats/{chat_id}/message', response_model=ChatModel, tags=['Chats'])
async def update_chat(response: Response,
                      chat_id: str = Depends(check_valid_chat_id),
                      chat: AddMessageRequest = None,
                      x_user_id: Optional[str] = Header(None),
                      x_api_key: Optional[str] = Header(None),
                      authorization: Optional[str] = Header(None),
                      x_request_id: Optional[str] = Header(None)):
    if authorization:
        response.headers['authorization'] = authorization
    log_request_body(x_request_id, chat)
    verify_api_key(x_api_key)
    _verify_user_id(x_user_id)
    _verify_ownership(chat_id, x_user_id)
    updated_chat = service.chat.add_message(chat_id, x_user_id, chat.message)
    if not updated_chat:
        raise ChatNotFound(chat_id)
    return updated_chat
