import logging
import os
from typing import Any, Optional

from fastapi import Request, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from jose import jwt, JWTError


from src.core.config import get_settings
from src.db.session import async_session_maker
from src.repository.user.get_by_id import get_by_id 

logger = logging.getLogger(__name__)


settings = get_settings()

class PanicCatcherMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: Any):
        try:
            response = await call_next(request)
            return response
        except SQLAlchemyError as error:
            logger.exception(
                "Database error during request processing",
                extra={"path": request.url.path},
            )
            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "type": "database_error",
                        "message": "Database operation failed.",
                        "detail": str(error),
                    }
                },
            )
        except Exception as error:  
            logger.exception(
                "Unhandled error during request processing",
                extra={"path": request.url.path},
            )
            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "type": "internal_error",
                        "message": "Unexpected server error.",
                        "detail": str(error),
                    }
                },
            )


class AuthMiddleware(BaseHTTPMiddleware):
 
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        
        # ⚠️ УКАЖИТЕ ЗДЕСЬ ВСЕ ПУБЛИЧНЫЕ ПУТИ (те, что не требуют токена)
        public_paths = [
            "/users/login",     # Ваши роуты начинаются с /users
            "/users/register",
            "/docs",
            "/openapi.json",
            "/redoc"
        ]
        
        # Пропускаем публичные пути и статику
        if request.url.path in public_paths or request.url.path.startswith("/static"):
            return await call_next(request)

        auth_header: Optional[str] = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return self._unauthorized_response("Bearer token required")
        
        token = auth_header.split(" ")[1]
        
        try:
            # 1. Декодируем токен
            payload = jwt.decode(
                token, 
                settings.jwt_secret_key, 
                algorithms=[settings.jwt_algorithm]
            )
            user_id_str = payload.get("sub")
            
            if user_id_str is None:
                return self._unauthorized_response("Token has no user ID")

            user_id = int(user_id_str)

        
            async with async_session_maker() as db:
                user = await get_by_id(db, user_id)
                
                if user is None: 
                    return self._unauthorized_response("User not found or inactive")

         
            request.state.user_id = user_id

        except JWTError:
            return self._unauthorized_response("Invalid or expired token")
        except SQLAlchemyError:
            logger.error("DB Error during auth check")
            return JSONResponse(status_code=500, content={"detail": "Auth DB Error"})
        except Exception as e:
            logger.error(f"Auth error: {e}")
            return self._unauthorized_response("An authentication error occurred")

        response = await call_next(request)
        return response

    def _unauthorized_response(self, detail: str) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": detail, "code": "UNAUTHORIZED"},
            headers={"WWW-Authenticate": "Bearer"},
        )