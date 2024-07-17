
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.routers.albums.album_schema import AlbumPhotoRead, AlbumRead
from app.routers.albums.album_service import AlbumService
from app.security.dependencies import get_album_service
from pymongo.errors import PyMongoError


class AlbumEndpoint:

    def __init__(self) -> None:
        self.album_router = APIRouter(tags=['Albums'], prefix='/albums')
        self.register_album_routes()

    def register_album_routes(self):
        self.album_router.get('/all', response_model=List[AlbumRead])(self.fetch_all_albums)
        self.album_router.get('/{album_id}', response_model=AlbumRead)(self.fetch_album_by_id)
        self.album_router.get('', response_model=List[AlbumRead])(self.fetch_limited_albums)
        self.album_router.get('/{album_id}/photos', response_model=AlbumPhotoRead)(self.fetch_album_photos)


    async def fetch_all_albums(self, album_service: AlbumService = Depends(get_album_service)) -> List[AlbumRead]:
        """
            Fetches all the albums.

            Args:
                album_service (AlbumService): Defaults to Depends(get_album_service)

            Returns:
                A list of albums based on the AlbumRead schema.
        """
        try:
            all_albums = await album_service.get_all_albums()
            return all_albums
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')

    async def fetch_album_by_id(self, album_id: int, album_service: AlbumService = Depends(get_album_service)) -> AlbumRead:
        """
            Fetches an album by its id.

            Args:
                album_id (int): The id of the album to get
                album_service (AlbumService): Defaults to Depends(get_album_service)

            Return:
                An album with the AlbumRead schema.
        """
        try:
            album = await album_service.get_album_by_id(album_id=album_id)
            if not album:
                raise HTTPException(detail="Album Not Found", status_code=status.HTTP_404_NOT_FOUND)
            return album
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def fetch_limited_albums(self, skip: int = 0, limit: int = 10, album_service: AlbumService = Depends(get_album_service)) -> List[AlbumRead]:
        """
            Fetches a list of albums depending on the number of albums to
            skip and the maximum number of albums to get

            Args:
                skip (int): The number of albums to skip
                limit (int): Maximum number of albums to obtain
                album_service (AlbumService): Defaults to Depends(get_album_service).

            Returns:
                A list of albums based on the AlbumRead schema.
        """
        try:
            limited_albums = await album_service.get_specific_albums(skip=skip, limit=limit)
            return limited_albums
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')

    async def fetch_album_photos(self, album_id: int, album_service: AlbumService = Depends(get_album_service)):
        """
            Fetches the album and their photos.

            Args:
                album_id (int): Gets the id of the album
                album_service (AlbumService): Defaults to Depends(get_album_service)

            Returns:
                An album with a list of photos associated with that album
                based on the AlbumPhotoRead schema.
        """
        try:
            album_photos = await album_service.get_album_photos(album_id=album_id)
            if not album_photos:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
            return album_photos
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')