import imp
from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    """Contains User model admin page config"""
    list_display = ("id", "username", "email", "password")


class AuctionAdmin(admin.ModelAdmin):
    """Contains Auction model admin page config"""
    list_display = ("id", "title", "created_by", "start_price", "active")


class BidAdmin(admin.ModelAdmin):
    """Contains Bid model admin page config"""
    list_display = ("user_name", "price", "auction")


class CommentAdmin(admin.ModelAdmin):
    """Contains Comment model admin page config"""
    list_display = ("user_name", "text", "auction")


admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)

