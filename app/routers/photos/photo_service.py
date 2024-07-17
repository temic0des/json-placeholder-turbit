from typing import List

from pydantic_core import Url
from app.routers.photos.photo_interface import IPhoto
from app.routers.photos.photo_model import Photo


class PhotoService(IPhoto):

    @staticmethod
    async def get_all_photos() -> List[Photo]:
        """
            Gets all the photos

            Returns:
                A list of photos.
        """
        photos = await Photo.find_all().to_list()
        return photos

    @staticmethod
    async def add_photos(photo_list: List[dict]) -> List[Photo]:
        """
            Inserts a list of photos to the database.

            Args:
                photo_list (List[dict]): Gets a list of photos

            Returns:
                photos based on the Photo Model
        """
        photos = [Photo(**photo) for photo in photo_list]
        try:
            # Insert list of Photo to the db
            await Photo.insert_many(photos)
            return photos
        except Exception as e:
            return e
    
    @staticmethod
    async def get_specific_photos(skip: int, limit: int) -> List[Photo]:
        """
            Get a limited list of photos

            Args:
                skip (int): The number of photos to skip
                limit (int): Maximum number of photos to obtain
            
            Returns:
                A list of photos based on the Photo Model
        """
        limited_photos = await Photo.find(skip=skip, limit=limit).to_list()
        return limited_photos
    
    @staticmethod
    async def get_photo_by_id(photo_id: int) -> Photo:
        """
            Get photo by the id

            Args:
                photo_id (int): The id of the photo to get

            Returns:
                photo based on the Photo Model
        """
        photo = await Photo.find_one(Photo.id == photo_id)
        if not photo:
            return None
        return photo