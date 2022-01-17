from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing/", views.CreateListingView.as_view(), name="create-listing"),
    path("auction-detail/<int:pk>", views.AuctionDetailView.as_view(), name="auction-detail")
]
