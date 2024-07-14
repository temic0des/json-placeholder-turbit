from typing import Annotated

from pydantic import BaseModel, UrlConstraints
from pydantic_core import Url

from app.common.seed_data.seed_data import SeedData


class APIUrlSchema(BaseModel):

    name: str
    url: Annotated[
        Url,
        UrlConstraints(max_length=2083, allowed_schemes=["http", "https"]),
    ]


API_URLS = [
    {"name": "user_url", "url": "https://jsonplaceholder.typicode.com/users"},
    {"name": "post_url", "url": "https://jsonplaceholder.typicode.com/posts"},
    {"name": "comment_url", "url": "https://jsonplaceholder.typicode.com/comments"},
    {"name": "album_url", "url": "https://jsonplaceholder.typicode.com/albums"},
    {"name": "photo_url", "url": "https://jsonplaceholder.typicode.com/photos"},
    {"name": "todo_url", "url": "https://jsonplaceholder.typicode.com/todos"},
]

async def run_seed():
    for api_urls in API_URLS:
        api_url_schema = APIUrlSchema(**api_urls)

        match api_url_schema.name:
            case 'user_url':
                user_seed = SeedData(url=str(api_url_schema.url))
                await user_seed.user_seed()
            case 'comment_url':
                comment_seed = SeedData(url=str(api_url_schema.url))
                await comment_seed.comment_seed()
            case 'post_url':
                post_seed = SeedData(url=str(api_url_schema.url))
                await post_seed.post_seed()
            case 'album_url':
                album_seed = SeedData(url=str(api_url_schema.url))
                await album_seed.album_seed()
            
    