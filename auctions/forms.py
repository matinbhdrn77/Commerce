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


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        exclude = ["created_by", "date", "active"]
        labels = {
            "title": "Product Name:",
            "start_price": "Price:",
            "image": "Product Image",
            "categories": "Chosse Categories:",
            "description": "Your Description:"
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["price"]
        labels = {
            "price": "Your Price:"
        }