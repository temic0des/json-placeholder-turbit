from typing import List
from app.routers.albums.album_interface import IAlbum
from app.routers.albums.album_model import Album
from app.routers.albums.album_schema import AlbumCreate


class AlbumService(IAlbum):

    @staticmethod
    async def add_albums(album_list: List[dict]) -> List[Album]:
        albums = [Album(**album) for album in album_list]
        await Album.insert_many(albums)
        return albums
       
        
    @staticmethod
    async def get_all_albums() -> List[Album]:
        return await Album.find_all().to_list()
    
    @staticmethod
    async def get_specific_albums(skip: int, limit: int) -> List[Album]:
        limited_albums = await Album.find(skip=skip, limit=limit).to_list()
        return limited_albums
    
    @staticmethod
    async def get_album(id: int) -> Album:
        album = await Album.find_one(Album.id == id)
        if not album:
            return None
        return album