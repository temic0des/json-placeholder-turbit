from fastapi import APIRouter
from app.routers.comments.comment_endpoint import CommentEndpoint
from app.routers.posts.post_endpoint import PostEndpoint
from app.routers.users.user_endpoint import UserEndpoint
from app.utils.settings import settings

router = APIRouter(prefix=settings.api_v1)
user_endpoint = UserEndpoint()
post_endpoint = PostEndpoint()
comment_endpoint = CommentEndpoint()
router.include_router(router=user_endpoint.user_router)
router.include_router(router=post_endpoint.post_router)
router.include_router(router=comment_endpoint.comment_router)