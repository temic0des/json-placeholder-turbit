from fastapi import APIRouter
from app.routers.users.user_endpoint import UserEndpoint
from app.utils.settings import settings

router = APIRouter(prefix=settings.api_v1)
user_endpoint = UserEndpoint()
router.include_router(router=user_endpoint.user_router)