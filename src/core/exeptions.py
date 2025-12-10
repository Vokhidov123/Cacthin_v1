# app/core/exceptions.py
from fastapi import HTTPException, status

class AppException(HTTPException):

    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class TaskNotFound(AppException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )


class PermissionDenied(AppException):
  
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещён"
        )


class InvalidData(AppException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверные данные"
        )
