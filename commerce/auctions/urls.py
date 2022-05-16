from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing/", views.create_listing, name="create_listing"),
    path("my_auctions/", views.my_auctions, name="my_auctions"),
    path("my_auctions/<str:uuid_auction>/edit_my_auctions", views.edit_my_auctions, name="edit_my_auctions"),
    path("bids/<str:uuid_product>", views.bids, name="bids"),
    path("categories/", views.categories, name="categories"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("mywatchlist/", views.mywatchlist, name="mywatchlist"),
    path("CloseConfirm/<str:uuid_product>", views.CloseConfirm, name="CloseConfirm"),
    path("Finished/<str:uuid_product>", views.Finished, name="Finished"),
]
