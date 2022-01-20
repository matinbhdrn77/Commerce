from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing/", views.CreateListingView.as_view(), name="create-listing"),
    path("auction-detail/<int:pk>", views.AuctionDetailView.as_view(), name="auction-detail"),
    path("close-auction/<int:pk>", views.CloseAuctionView.as_view(), name="close-auction"),
    path("watchlist/<int:id>", views.WatchListView.as_view(), name="watchlist"),
    path("show-watchlist/", views.ShowWatchlistView.as_view(), name="show-watchlist"),
    path("show-category/<str:categories>", views.ShowCategoriesView.as_view(), name="show-category")
]
