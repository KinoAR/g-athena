from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.views import generic
from django.urls import reverse
from .models import User, Game, GameReview
# Create your views here.

class HomeView(generic.ListView):
    template_name = "reviews/home.html"
    context_object_name = "latest_games_list"

    def get_queryset(self):
        return Game.objects.order_by("-publish_date")[:5]

class RegisterView(generic.FormView):
    template_name = "reviews/register.html"
    context_object_name = ""
            

class SearchResultsView(generic.TemplateView):
    template_name = "reviews/searchresults.html"
    context_object_name = ""

class GameView(generic.TemplateView):
    template_name = "reviews/game.html"
    context_object_name = ""

class ReviewView(generic.TemplateView):
    template_name = "reviews/review.html"
    context_object_name = ""
    
