from contextlib import nullcontext
from operator import mod
from pyexpat import model
from statistics import mode
from tkinter import Widget
from turtle import title
from typing_extensions import Required
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core import validators
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class User(AbstractUser):
    pass


CATEGORY = [
    ("Motors", "Motors"),
    ("Fashion", "Fashion"),
    ("Electronics", "Electronics"),
    ("Collectibles & Art", "Collectibles & Art"),
    ("Home & Garden", "Home & Garden"),
    ("Sporting Goods", "Sporting Goods"),
    ("Toys", "Toys"),
    ("Business & Industrial", "Business & Industrial"),
    ("Music", "Music"),
    ("NONE", "NONE")
]


class Auction(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="auctions")
    start_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators={MinValueValidator: 1.00})
    description = models.TextField(blank=True)
    date =models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images", null=True, blank=False)
    categories = models.CharField(
        max_length=255, choices=CATEGORY, default="NON")
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("auction-detail", args=[self.pk])
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=400)
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="comments")


class Bid(models.Model):
    user_name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators={MinValueValidator: 1.00})
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="bids")
    def get_absolute_url(self):
        return reverse("auction-detail", args=[self.auction.id])