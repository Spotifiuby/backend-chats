from pydantic import BaseModel
import datetime


class TokenModel(BaseModel):
    token: str
    user_id: str
    date_created: datetime.datetime


class UpdateTokenModel(BaseModel):
    token: str
