
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.routers.albums.album_schema import AlbumRead
from app.routers.albums.album_service import AlbumService
from app.security.dependencies import get_album_service
from pymongo.errors import PyMongoError


class AlbumEndpoint:

    def __init__(self) -> None:
        self.album_router = APIRouter(tags=['Albums'], prefix='/albums')
        self.register_album_routes()

    def register_album_routes(self):
        self.album_router.get('/all', response_model=List[AlbumRead])(self.get_all_albums)
        self.album_router.get('/{id}', response_model=AlbumRead)(self.get_album)
        self.album_router.get('', response_model=List[AlbumRead])(self.get_specific_albums)


    async def get_all_albums(self, album_service: AlbumService = Depends(get_album_service)) -> List[AlbumRead]:
        try:
            all_albums = await album_service.get_all_albums()
            return all_albums
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')

    async def get_album(self, id: int, album_service: AlbumService = Depends(get_album_service)) -> AlbumRead:
        try:
            album = await album_service.get_album(id=id)
            if not album:
                raise HTTPException(detail="Album Not Found", status_code=status.HTTP_404_NOT_FOUND)
            return album
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def get_specific_albums(self, skip: int = 0, limit: int = 10, album_service: AlbumService = Depends(get_album_service)) -> List[AlbumRead]:
        try:
            limited_albums = await album_service.get_specific_albums(skip=skip, limit=limit)
            return limited_albums
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
