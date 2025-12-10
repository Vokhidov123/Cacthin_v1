from fastapi import APIRouter


from src.handler.user.delete import router as delete_router
from src.handler.user.register import router as register_router
from src.handler.user.login import router as login_router
from src.handler.user.patch import router as patch_router
from src.handler.item.create import router as create_item
from src.handler.item.delete import router as delete_item
from src.handler.item.update import router as update_item
from src.handler.item.get_all import router as get_all_item
from src.handler.item.get_by_id import router as get_id_item


api_router = APIRouter()
api_router.include_router(delete_router)
api_router.include_router(register_router)
api_router.include_router(login_router)
api_router.include_router(patch_router)
api_router.include_router(create_item)
api_router.include_router(delete_item)
api_router.include_router(get_all_item)
api_router.include_router(get_id_item)
api_router.include_router(update_item)



