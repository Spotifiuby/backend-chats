from fastapi import HTTPException, status


class TokenNotFound(HTTPException):
    def __init__(self, user_id: str):
        super().__init__(status.HTTP_404_NOT_FOUND, f"Token not found for user {user_id}", None)
