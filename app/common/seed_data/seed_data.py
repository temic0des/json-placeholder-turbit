from app.routers.albums.album_model import Album
from app.routers.albums.album_service import AlbumService
from app.routers.comments.comment_service import CommentService
from app.routers.posts.post_model import Post
from app.routers.posts.post_service import PostService
from app.routers.users.user_service import UserService
from app.utils.api_request import APIRequest
from app.routers.users.user_model import User
from app.routers.comments.comment_model import Comment

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
        
    async def comment_seed(self):
        comment_data = self.api_request
        comment_list = comment_data.get_data()
        try:
            comment_count = await Comment.find_all().count()
            if comment_count > 0:
                return
            comments = await CommentService.add_comments(comment_list=comment_list)
            return comments
        except Exception as e:
            return e
        
    async def album_seed(self):
        album_data = self.api_request
        album_list = album_data.get_data()
        try:
            album_count = await Album.find_all().count()
            if album_count > 0:
                return
            albums = await AlbumService.add_albums(album_list=album_list)
            return albums
        except Exception as e:
            return e