from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.routers.posts.post_schema import PostRead
from app.routers.posts.post_service import PostService
from app.security.dependencies import get_post_service
from pymongo.errors import PyMongoError
class PostEndpoint:

    def __init__(self) -> None:
        self.post_router = APIRouter(tags=['Posts'], prefix='/posts')
        self.register_post_routes()

    def register_post_routes(self):
        self.post_router.get('/all', response_model=List[PostRead])(self.get_all_posts)
        self.post_router.get('', response_model=List[PostRead])(self.get_limited_posts)

    async def get_all_posts(self, post_service: PostService = Depends(get_post_service)) -> List[PostRead]:
        try:
            all_posts = await post_service.get_all_posts()
            return all_posts
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        
    async def get_limited_posts(self, skip: int = 0, limit: int = 10, post_service: PostService = Depends(get_post_service)) -> List[PostRead]:
        try:
            limited_posts = await post_service.get_specific_posts(skip=skip, limit=limit)
            return limited_posts
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')