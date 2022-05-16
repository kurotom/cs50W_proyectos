
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("createpost", views.createpost, name="createpost"),
    path("posts", views.posts, name="posts"),
    path("likedpost/<int:idpost>", views.likedpost, name= "likedpost"),
    path("following", views.following, name="following"),
    path("postedit/<int:idpost>", views.postedit, name="postedit"),
    path("userview/<str:username>", views.userview, name="userview"),
    path("createFollowing/<str:following>", views.createFollowing, name="createFollowing"),
]
