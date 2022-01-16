from operator import mod
from pyexpat import model
from statistics import mode
from turtle import title
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core import validators
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Auction(models.Model):
    title = models.CharField(max_length=255)
    user_name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="auctions")
    start_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators={MinValueValidator: 1.00})
    date = models.DateField()
    categories = models.ManyToManyField(Category, related_name="auctions")
    active = models.BooleanField(default=True)

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
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")