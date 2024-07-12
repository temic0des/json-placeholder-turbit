from app.routers.posts.post_service import PostService
from app.routers.users.user_service import UserService

def get_user_service():
    return UserService()

def get_post_service():
    return PostService()