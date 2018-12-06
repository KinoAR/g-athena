from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.views import generic
from django.urls import reverse
from django.db.models import Q
from functools import reduce
from .models import User, Game, GameReview
from .forms import UserForm, ReviewForm
# Create your views here.

class HomeView(generic.ListView):
    template_name = "reviews/home.html"
    context_object_name = "latest_games_list"

    def get_queryset(self):
        return Game.objects.order_by("-publish_date")[:5]

class RegisterView(generic.FormView):
    form_class = UserForm
    template_name = "reviews/register.html"
    context_object_name = "form"


class SearchResultsView(generic.ListView):
    model = Game
    template_name = "reviews/searchresults.html"
    context_object_name = "searched_games_list"

    def get_queryset(self, **kwargs):
        context = super().get_queryset(**kwargs)
        search_string = self.kwargs.get('search')
        print(search_string)
        list = search_string.split(sep=" ")
        return Game.objects.filter(
            reduce(lambda x, y: x | y, [Q(name__contains=word) for word in list])
        )

class GameView(generic.DetailView):
    model = Game
    template_name = "reviews/game.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter is used to show more than one data in the view
        context['reviews_list'] = GameReview.objects.filter(game_id=self.kwargs.get('pk'))
        # self.reviews_list = 
        return context
    

class ReviewView(generic.FormView):
    model = Game
    form_class = ReviewForm
    template_name = "reviews/review.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game'] = Game.objects.get(game_id=self.kwargs.get('pk'))
        return context