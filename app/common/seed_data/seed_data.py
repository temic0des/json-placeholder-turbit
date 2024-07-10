from app.routers.posts.post_model import Post
from app.routers.posts.post_service import PostService
from app.routers.users.user_service import UserService
from app.utils.api_request import APIRequest
from app.routers.users.user_model import User

class SeedData:

    def __init__(self, url) -> None:
        self._url = url
        self.api_request = APIRequest(url=self._url)

    @property
    def url(self):
        return self._url

    async def user_seed(self):
        user_data = self.api_request
        user_list = user_data.get_data()
        try:
            user_count = await User.find_all().count()
            if user_count > 0:
                return
            users = await UserService.add_users(user_list=user_list)
            return users
        except Exception as e:
            return e
        
    async def post_seed(self):
        post_data = self.api_request
        post_list = post_data.get_data()
        try:
            post_count = await Post.find_all().count()
            if post_count > 0:
                return
            posts = await PostService.add_posts(post_list=post_list)
            return posts
        except Exception as e:
            return e