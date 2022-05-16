from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new_wiki", views.new_wiki, name="new_wiki"),
    path("random_page/", views.random_page, name="random_page"),
    path("<str:name_title>/edit", views.name_title, name="name_title"),
    re_path(r'(?P<busqueda>)', views.busqueda, name="busqueda"),
]

