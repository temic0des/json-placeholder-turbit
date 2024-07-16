from fastapi import APIRouter
from app.routers.albums.album_endpoint import AlbumEndpoint
from app.routers.comments.comment_endpoint import CommentEndpoint
from app.routers.photos.photo_endpoint import PhotoEndpoint
from app.routers.posts.post_endpoint import PostEndpoint
from app.routers.todos.todo_endpoint import TodoEndpoint
from app.routers.users.user_endpoint import UserEndpoint
from app.utils.settings import settings

router = APIRouter(prefix=settings.api_v1)
user_endpoint = UserEndpoint()
post_endpoint = PostEndpoint()
comment_endpoint = CommentEndpoint()
album_endpoint = AlbumEndpoint()
photo_endpoint = PhotoEndpoint()
todo_endpoint = TodoEndpoint()

router.include_router(router=user_endpoint.user_router)
router.include_router(router=post_endpoint.post_router)
router.include_router(router=comment_endpoint.comment_router)
router.include_router(router=album_endpoint.album_router)
router.include_router(router=photo_endpoint.photo_router)
router.include_router(router=todo_endpoint.todo_router)