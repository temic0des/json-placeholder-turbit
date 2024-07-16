from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.routers.posts.post_schema import PostCommentRead, PostRead
from app.routers.posts.post_service import PostService
from app.security.dependencies import get_post_service
from pymongo.errors import PyMongoError
class PostEndpoint:

    def __init__(self) -> None:
        self.post_router = APIRouter(tags=['Posts'], prefix='/posts')
        self.register_post_routes()

    def register_post_routes(self):
        self.post_router.get('/all', response_model=List[PostRead])(self.fetch_all_posts)
        self.post_router.get('/{post_id}', response_model=PostRead)(self.fetch_post_by_id)
        self.post_router.get('', response_model=List[PostRead])(self.fetch_limited_posts)
        self.post_router.get('/{post_id}/comments', response_model=PostCommentRead)(self.fetch_comments_by_post)

    async def fetch_all_posts(self, post_service: PostService = Depends(get_post_service)) -> List[PostRead]:
        try:
            all_posts = await post_service.get_all_posts()
            return all_posts
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def fetch_post_by_id(self, post_id: int, post_service: PostService = Depends(get_post_service)) -> PostRead:
        try:
            post = await post_service.get_post_by_id(post_id=post_id)
            if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
            return post
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def fetch_limited_posts(self, skip: int = 0, limit: int = 10, post_service: PostService = Depends(get_post_service)) -> List[PostRead]:
        try:
            limited_posts = await post_service.get_specific_posts(skip=skip, limit=limit)
            return limited_posts
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def fetch_comments_by_post(self, post_id: int, post_service: PostService = Depends(get_post_service)) -> List[PostCommentRead]:
        try:
            post_comments = await post_service.get_comments_by_post(post_id=post_id)
            if not post_comments:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
            return post_comments
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')