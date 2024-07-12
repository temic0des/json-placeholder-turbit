from fastapi import APIRouter
from app.routers.posts.post_endpoint import PostEndpoint
from app.routers.users.user_endpoint import UserEndpoint
from app.utils.settings import settings

router = APIRouter(prefix=settings.api_v1)
user_endpoint = UserEndpoint()
post_endpoint = PostEndpoint()
router.include_router(router=user_endpoint.user_router)
router.include_router(router=post_endpoint.post_router)