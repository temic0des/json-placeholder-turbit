from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import PyMongoError

from app.routers.photos.photo_schema import PhotoRead
from app.routers.photos.photo_service import PhotoService
from app.security.dependencies import get_photo_service


class PhotoEndpoint:

    def __init__(self) -> None:
        self.photo_router = APIRouter(tags=['Photos'], prefix='/photos')
        self.register_photo_routes()

    def register_photo_routes(self):
        self.photo_router.get('/all', response_model=List[PhotoRead])(self.fetch_all_photos)
        self.photo_router.get('/{photo_id}', response_model=PhotoRead)(self.fetch_photo_by_id)
        self.photo_router.get('', response_model=List[PhotoRead])(self.fetch_limited_photos)

    async def fetch_all_photos(self, photo_service: PhotoService = Depends(get_photo_service)) -> List[PhotoRead]:
        """
            Fetches all the photos

            Args:
                photo_service (PhotoService): Defaults to Depends(get_photo_service)

            Returns:
                A list of photos using the PhotoRead schema
        """
        try:
            all_photos = await photo_service.get_all_photos()
            return all_photos
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def fetch_photo_by_id(self, photo_id: int, photo_service: PhotoService = Depends(get_photo_service)) -> PhotoRead:
        """
            Fetches the photo by id.

            Args:
                photo_id (int): Gets the id of the photo
                photo_service (PhotoService): Defaults to Depends(get_photo_service)

            Returns:
                A photo using the PhotoRead schema.
        """
        try:
            photo = await photo_service.get_photo_by_id(photo_id=photo_id)
            if not photo:
                raise HTTPException(detail="Photo not found", status_code=status.HTTP_404_NOT_FOUND)
            return photo
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def fetch_limited_photos(self, skip: int = 0, limit: int = 10, photo_service: PhotoService = Depends(get_photo_service)):
        """
            Fetches a list of photos depending on the number of photos to
            skip and the maximum number of photos to get

            Args:
                skip (int): The number of photos to skip
                limit (int): Maximum number of photos to obtain
                photo_service (PhotoService): Defaults to Depends(get_photo_service).

            Returns:
                A list of photos based on the PhotoRead schema.
        """
        try:
            limited_photos = await photo_service.get_specific_photos(skip=skip, limit=limit)
            return limited_photos
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
