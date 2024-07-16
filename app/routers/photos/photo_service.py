from typing import List

from pydantic_core import Url
from app.routers.photos.photo_interface import IPhoto
from app.routers.photos.photo_model import Photo


class PhotoService(IPhoto):

    @staticmethod
    async def get_all_photos() -> List[Photo]:
        photos = await Photo.find_all().to_list()
        return photos

    @staticmethod
    async def add_photos(photo_list: List[dict]) -> List[Photo]:
        photos = [Photo(**photo) for photo in photo_list]
        try:
            await Photo.insert_many(photos)
            return photos
        except Exception as e:
            return e
    
    @staticmethod
    async def get_specific_photos(skip: int, limit: int) -> List[Photo]:
        limited_photos = await Photo.find(skip=skip, limit=limit).to_list()
        return limited_photos
    
    @staticmethod
    async def get_photo(id: int) -> Photo:
        photo = await Photo.find_one(Photo.id == id)
        return photo