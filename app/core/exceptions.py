from typing import Any
from typing import Dict
from typing import Optional

from fastapi import HTTPException
from fastapi import status

from app.core.telemetry import logger


class BadRequestError(HTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, str]] = None) -> None:
        logger.info(detail, extra={"exception_type": "BadRequestError"})
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, headers)


class AuthError(HTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, str]] = None) -> None:
        logger.info(detail, extra={"exception_type": "AuthError"})
        super().__init__(status.HTTP_403_FORBIDDEN, detail, headers)


class NotFoundError(HTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, str]] = None) -> None:
        logger.info(detail, extra={"exception_type": "NotFoundError"})
        super().__init__(status.HTTP_404_NOT_FOUND, detail, headers)


class ValidationError(HTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        logger.info(detail, extra={"exception_type": "ValidationError"})
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, detail, headers)


class DuplicatedError(HTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        logger.info(detail, extra={"exception_type": "DuplicatedError"})
        super().__init__(status.HTTP_409_CONFLICT, detail, headers)


class InvalidCredentials(HTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        logger.info(detail, extra={"exception_type": "InvalidCredentials"})
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, headers)
