
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("manage_post",views.manage_post,name="manage_post"),
    path("editUserStatus/<int:id>",views.editUserStatus,name="editUserStatus"),
    path("profile_view/<int:id>",views.profile_view,name="profile_view"),
    path("following_post",views.following_post,name="following_post"),
    path("fetch_posts/<str:user>",views.fetch_posts,name="fetch_posts"),
    path("fetch_users/<str:users>",views.fetch_users,name="fetch_users"),
    path("update_post/<int:postId>",views.update_post,name="update_post"),
]
