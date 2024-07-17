from typing import List
from app.routers.albums.album_interface import IAlbum
from app.routers.albums.album_model import Album
from app.routers.albums.album_schema import AlbumPhotoRead
from app.routers.photos.photo_model import Photo
from app.routers.photos.photo_schema import PhotoRead


class AlbumService(IAlbum):

    @staticmethod
    async def add_albums(album_list: List[dict]) -> List[Album]:
        """
            Create a list of albums into the database.

            Args:
                album_list (List[dict]): The list of albums to be sent

            Returns:
                The list of Album
        """
        albums = [Album(**album) for album in album_list]
        try:
            await Album.insert_many(albums)
            return albums
        except Exception as e:
            return e
       
        
    @staticmethod
    async def get_all_albums() -> List[Album]:
        """
            Gets all the albums

            Returns:
                A list of albums.
                This is returned based on the Album schema.
        """
        return await Album.find_all().to_list()
    
    @staticmethod
    async def get_specific_albums(skip: int, limit: int) -> List[Album]:
        """
            Get a subset of albums

            Args:
                skip (int): The number of albums to skip
                limit (int): Maximum number of albums to obtain

            Returns:
                A list of albums with the AlbumRead schema
        """
        limited_albums = await Album.find(skip=skip, limit=limit).to_list()
        return limited_albums
    
    @staticmethod
    async def get_album_by_id(album_id: int) -> Album:
        """
            Gets a album by its id

            Args:
                album_id (int): The id of the album to get

            Returns:
                The album to get
                This is returned as an instance of the AlbumRead
                schema.
        """
        album = await Album.find_one(Album.id == album_id)
        if not album:
            return None
        return album
    
    @staticmethod
    async def get_album_photos(album_id: int) -> AlbumPhotoRead:
        """
            Get all the photos associated with a album

            Args:
                album_id (int): The id of the album

            Return:
                The album and the photos associated with the album.
                The is returned based on the AlbumPhotoRead schema.
        """
        # Get the album by the album_id
        album = await Album.find_one(Album.id == album_id)
        if not album:
            return None
        # Get all the photos by the album_id
        photos = await Photo.find(Photo.album_id == album_id).to_list()
        photos_read = [PhotoRead(**photo.model_dump()) for photo in photos[:100]]
        # Album and the photos using the AlbumPhotoRead schema
        album_photos = AlbumPhotoRead(**album.model_dump(), photos=photos_read)
        return album_photos