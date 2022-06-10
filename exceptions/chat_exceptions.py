from fastapi import HTTPException, status


class ChatNotFound(HTTPException):
    def __init__(self, chat_id: str):
        super().__init__(status.HTTP_404_NOT_FOUND, f"Chat {chat_id} not found", None)


class ChatNotOwnedByUser(HTTPException):
    def __init__(self, chat_id: str, user_id: str):
        super().__init__(status.HTTP_400_BAD_REQUEST, f"The owner of chat {chat_id} is not {user_id}", None)
