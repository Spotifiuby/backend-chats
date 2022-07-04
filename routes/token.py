from fastapi import APIRouter, status, Header, Response
from typing import Optional

from utils.utils import log_request_body, verify_api_key
from models.token import TokenModel, UpdateTokenModel
import service.token
from exceptions.user_exceptions import MissingUserId
from exceptions.token_exceptions import TokenNotFound

token_routes = APIRouter()


def _verify_user_id(user_id):
    if not user_id:
        raise MissingUserId()
    return user_id


@token_routes.get('/token', response_model=TokenModel, tags=['Token'], status_code=status.HTTP_200_OK)
async def get_token(response: Response,
                    x_user_id: Optional[str] = Header(None),
                    x_api_key: Optional[str] = Header(None),
                    authorization: Optional[str] = Header(None)):
    if authorization:
        response.headers['authorization'] = authorization
    verify_api_key(x_api_key)
    _verify_user_id(x_user_id)
    token = service.token.get_token(x_user_id)
    if not token:
        raise TokenNotFound(x_user_id)

    return token


@token_routes.post('/token', response_model=TokenModel, tags=['Token'], status_code=status.HTTP_201_CREATED)
async def update_token(response: Response,
                       token: UpdateTokenModel,
                       x_user_id: Optional[str] = Header(None),
                       x_api_key: Optional[str] = Header(None),
                       authorization: Optional[str] = Header(None),
                       x_request_id: Optional[str] = Header(None)):
    if authorization:
        response.headers['authorization'] = authorization
    log_request_body(x_request_id, token)
    verify_api_key(x_api_key)
    _verify_user_id(x_user_id)
    return service.token.create(x_user_id, token.token)
