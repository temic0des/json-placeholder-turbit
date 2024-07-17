from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.routers.comments.comment_schema import CommentRead
from app.routers.comments.comment_service import CommentService
from app.security.dependencies import get_comment_service
from pymongo.errors import PyMongoError


class CommentEndpoint:

    def __init__(self) -> None:
        self.comment_router = APIRouter(tags=['Comments'], prefix='/comments')
        self.register_comment_routes()

    def register_comment_routes(self):
        self.comment_router.get('/all', response_model=List[CommentRead])(self.fetch_all_comments)
        self.comment_router.get('/{comment_id}', response_model=CommentRead)(self.fetch_comment_by_id)
        self.comment_router.get('', response_model=List[CommentRead])(self.fetch_limited_comments)

    async def fetch_all_comments(self, comment_service: CommentService = Depends(get_comment_service)) -> List[CommentRead]:
        """
            Fetches all the comments

            Args:
                comment_service (CommentService): Defaults to Depends(get_comment_service)

            Returns:
                A list of comments using the CommentRead schema
        """
        try:
            all_comments = await comment_service.get_all_comments()
            return all_comments
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')

    async def fetch_comment_by_id(self, comment_id: int, comment_service: CommentService = Depends(get_comment_service)) -> CommentRead:
        """
            Fetches the comment by id.

            Args:
                comment_id (int): Gets the id of the comment
                comment_service (CommentService): Defaults to Depends(get_comment_service)

            Returns:
                A comment using the CommentRead schema.
        """
        try:
            comment = await comment_service.get_comment_by_id(comment_id=comment_id)
            return comment
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def fetch_limited_comments(self, skip: int = 0, limit: int = 10, comment_service: CommentService = Depends(get_comment_service)):
        """
            Fetches a list of comments depending on the number of comments to
            skip and the maximum number of comments to get

            Args:
                skip (int): The number of comments to skip
                limit (int): Maximum number of comments to obtain
                comment_service (CommentService): Defaults to Depends(get_comment_service).

            Returns:
                A list of comments based on the CommentRead schema.
        """
        try:
            limited_comments = await comment_service.get_specific_comments(skip=skip, limit=limit)
            return limited_comments
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')