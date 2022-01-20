from contextlib import redirect_stderr
from operator import mod
from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic import ListView, DetailView, View, TemplateView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

import auctions


from .forms import AuctionForm, BidForm, CommentForm
from .models import Auction, User


class IndexView(ListView):
    template_name = "auctions/index.html"
    model = Auction
    context_object_name = "auctions"


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
        bids = auction.bids.order_by("-price")
        context["auction"] = auction
        context["total_bid"] = bids.count()

        # comments for auction
        comments = auction.comments.all()
        context["comments"] = comments
        context["comment_form"] = CommentForm()
        # retrun best suggest
        try:
            highest = bids.first()
            context["highest"] = highest.price
            context["best_suggest_user"] = highest.user_name
        except AttributeError:
            pass
        # Check item is watchlist
        if request.user in auction.users_watchlist.all():
            context["is_watch_list"] =  True
        else:
            context["is_watch_list"] =  False
    
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
            auction.current_price = highest
            auction.save()
            return super().form_valid(form)
        messages.error(
            self.request, 'Your Suggest must be greater than actual suggest')
        return HttpResponseRedirect(reverse("auction-detail", args=[auction_id]))


class CloseAuctionView(LoginRequiredMixin, View):
    def get(self, request, pk):
        auction = get_object_or_404(Auction, id=pk)
        auction.active = False
        auction.save()
        return HttpResponseRedirect(reverse("auction-detail", args=[pk]))


class WatchListView(LoginRequiredMixin, View):
    def get(self, request, id):
        auction = get_object_or_404(Auction, id=id)
        if request.user in auction.users_watchlist.all():
            auction.users_watchlist.remove(request.user)
        else:
            auction.users_watchlist.add(request.user)
        auction.save()
        return HttpResponseRedirect(reverse("auction-detail", args=[id]))


class ShowWatchlistView(LoginRequiredMixin, ListView):
    template_name = "auctions/index.html"
    model = Auction
    context_object_name = "auctions"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(users_watchlist=self.request.user).order_by("-date")


class ShowCategoriesView(LoginRequiredMixin, ListView):
    template_name = "auctions/index.html"
    model = Auction
    context_object_name = "auctions"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(categories=self.kwargs["categories"]).order_by("-date")


class HandleCommentView(View):
    def post(self, request, id):
        auction = get_object_or_404(Auction, id=id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user_name = request.user
            comment.auction = auction
            comment.save()
        else:
            messages.error(
            self.request, 'Your Suggest must be greater than actual suggest')
        return HttpResponseRedirect(reverse("auction-detail", args=[id]))