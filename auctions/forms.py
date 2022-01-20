from statistics import mode
from xml.etree.ElementInclude import include
from django import forms
from django.db import models

from .models import Comment, Auction, Bid


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {
            "text": "Your Comment:"
        }
        widgets = {
            "text": forms.Textarea(attrs={
                "class": "form-control"
            })
        }


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        exclude = ["created_by", "date", "active", "users_watchlist"]
        labels = {
            "title": "Product Name:",
            "current_price": "Price:",
            "image": "Product Image:",
            "categories": "Chosse Categories:",
            "description": "Your Description:"
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ["user_name", "auction"]
        labels = {
            "price": ''
        }
        widgets = {
            "price": forms.NumberInput(attrs={
                "placeholder": "Bid",
                "min": 0.01,
                "max": 100000000000,
                "class": "form-control"
            })
        }
        error_messages = {
            "price": {
                "required": "Your price must be filled",
                
            }
        }