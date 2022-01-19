from contextlib import redirect_stderr
from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

import auctions


from .forms import AuctionForm, BidForm
from .models import Auction, User


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


class CreateListingView(LoginRequiredMixin, CreateView):
    form_class = AuctionForm
    template_name = "auctions/create-listing.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class AuctionDetailView(CreateView):
    template_name = "auctions/detail-auction.html"
    form_class = BidForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        auction = get_object_or_404(Auction, id=self.kwargs.get("pk"))
        self.kwargs["auction"] = auction
        bids = auction.bids.order_by("-price")
        context["auction"] = auction
        context["total_bid"] = bids.count()
        try:
            highest = bids.first()
            context["highest"] = highest.price
            context["best_suggest_user"] = highest.user_name
        except AttributeError:
            pass
        try:
            watch_list_id = request.session["watch_list"]
            context["is_watch_list"] = watch_list_id == str(auction.id)
        except KeyError:
            pass
        return context

    def form_valid(self, form, **kwargs):
        auction_id = self.request.POST.get("auction_id")
        auction = get_object_or_404(Auction, id=auction_id)
        try:
            highest = auction.bids.order_by("-price").first().price
        except:
            highest = auction.start_price
        price = float(form.cleaned_data["price"])
        if price > highest:
            form.instance.user_name = self.request.user
            form.instance.auction = auction
            return super().form_valid(form)
        messages.error(self.request, 'Your Suggest must be greater than actual suggest')
        return HttpResponseRedirect(reverse("auction-detail", args=[auction_id]))


class CloseAuctionView(View):
    def get(self, request, pk):
        auction = get_object_or_404(Auction, id=pk)
        auction.active = False
        auction.save()
        return HttpResponseRedirect(reverse("auction-detail", args=[pk]))
