from app.routers.albums.album_service import AlbumService
from app.routers.comments.comment_service import CommentService
from app.routers.photos.photo_service import PhotoService
from app.routers.posts.post_service import PostService
from app.routers.todos.todo_service import TodoService
from app.routers.users.user_service import UserService

def get_user_service():
    return UserService()

def get_post_service():
    return PostService()

def get_comment_service():
    return CommentService()

def get_album_service():
    return AlbumService()

def get_photo_service():
    return PhotoService()

def get_todo_service():
    return TodoService()