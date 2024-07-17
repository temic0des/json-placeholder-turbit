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
        """
            Fetches all the posts.

            Args:
                post_service (PostService): Defaults to Depends(get_post_service)

            Returns:
                A list of posts based on the PostRead schema.
        """
        try:
            # Get all the posts
            all_posts = await post_service.get_all_posts()
            return all_posts
        except PyMongoError as e:
            # Raises an exception if an error occurs while interacting with the database
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            # Catches other exceptions
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def fetch_post_by_id(self, post_id: int, post_service: PostService = Depends(get_post_service)) -> PostRead:
        """
            Fetches a post by its id.

            Args:
                post_id (int): The id of the post to get
                post_service (PostService): Defaults to Depends(get_post_service)

            Return:
                A post with the PostRead schema.
        """
        try:
            # Get a post by the post_id
            post = await post_service.get_post_by_id(post_id=post_id)
            if not post:
                # Raises an exception of the post does not exist
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
            return post
        except PyMongoError as e:
            # Raises an exception if an error occurs while interacting with the database
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            # Catches other exceptions
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def fetch_limited_posts(self, skip: int = 0, limit: int = 10, post_service: PostService = Depends(get_post_service)) -> List[PostRead]:
        """
            Fetches a list of posts depending on the number of posts to
            skip and the maximum number of comments to get

            Args:
                skip (int): The number of posts to skip
                limit (int): Maximum number of posts to obtain
                post_service (PostService): Defaults to Depends(get_post_service).

            Returns:
                A list of posts based on the PostRead schema.
        """
        try:
            limited_posts = await post_service.get_specific_posts(skip=skip, limit=limit)
            return limited_posts
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def fetch_comments_by_post(self, post_id: int, post_service: PostService = Depends(get_post_service)) -> PostCommentRead:
        """
            Fetches the post and their comments.

            Args:
                post_id (int): Gets the id of the post
                post_service (PostService): Defaults to Depends(get_post_service)

            Returns:
                A post with all the comments associated with that post
                based on the PostCommentRead schema.
        """
        try:
            # Get post and the list of comments
            post_comments = await post_service.get_comments_by_post(post_id=post_id)
            if not post_comments:
                # Raises exception if the post is not found.
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
            return post_comments
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')