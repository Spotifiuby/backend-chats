from pydantic import BaseModel
import datetime


class Message(BaseModel):
    sender: str
    text: str
    time: datetime.datetime


class ChatModel(BaseModel):
    id: str
    users: list[str]
    messages: list[Message]
    date_created: datetime.datetime


class CreateChatRequest(BaseModel):
    user: str


class AddMessageRequest(BaseModel):
    message: str
