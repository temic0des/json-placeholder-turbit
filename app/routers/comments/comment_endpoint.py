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
        self.comment_router.get('/all', response_model=List[CommentRead])(self.get_all_comments)
        self.comment_router.get('', response_model=CommentRead)(self.get_comment)
        self.comment_router.get('', response_model=List[CommentRead])(self.get_limited_comments)

    async def get_all_comments(self, comment_service: CommentService = Depends(get_comment_service)) -> List[CommentRead]:
        try:
            all_comments = await comment_service.get_all_comments()
            return all_comments
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')

    async def get_comment(self, id: int, comment_service: CommentService = Depends(get_comment_service)) -> CommentRead:
        try:
            comment = await comment_service.get_comment(id=id)
            return comment
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        
    async def get_limited_comments(self, skip: int = 0, limit: int = 10, comment_service: CommentService = Depends(get_comment_service)):
        try:
            limited_comments = await comment_service.get_specific_comments(skip=skip, limit=limit)
            return limited_comments
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')