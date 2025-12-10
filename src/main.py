

from fastapi import FastAPI

from src.core.config import get_settings

from src.core.logging_config import configure_logging 

from src.core.middleware import PanicCatcherMiddleware, AuthMiddleware
from src.handler.router import api_router

settings = get_settings()
configure_logging(settings)


app = FastAPI(
    title=settings.project_name,
    debug=settings.debug,
)


app.add_middleware(AuthMiddleware)


app.add_middleware(PanicCatcherMiddleware)


app.include_router(api_router)