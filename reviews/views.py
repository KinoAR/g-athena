from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views import generic
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import authenticate, login
from functools import reduce
from .models import User, Game, GameReview
from .forms import UserForm, ReviewForm
from django.utils import timezone
# Create your views here.

class HomeView(generic.ListView):
    template_name = "reviews/home.html"
    context_object_name = "latest_games_list"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['member_id']
        context['localUser'] = User.objects.get(user_id=userid)
        return context

    def get_queryset(self):
        return Game.objects.order_by("-publish_date")[:5]

class RegisterView(generic.FormView):
    form_class = UserForm
    template_name = "reviews/register.html"
    success_url = "/reviews/login/"

    def form_valid(self, form):
        user = User.objects.create(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password'],
            creation_date = timezone.now()
        )
        return super().form_valid(form)


class LoginView(generic.FormView):
    form_class = UserForm
    template_name = "reviews/login.html"
    success_url = "/reviews/"

    def form_valid(self, form):
        m = User.objects.get(username=form.cleaned_data['username'])
        if m.password == form.cleaned_data['password']:
            self.request.session['member_id'] = m.user_id
        return super().form_valid(form)

class SearchResultsView(generic.ListView):
    model = Game
    template_name = "reviews/searchresults.html"
    context_object_name = "searched_games_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['member_id']
        context['localUser'] = User.objects.get(user_id=userid)
        return context

    def get_queryset(self, **kwargs):
        context = super().get_queryset(**kwargs)
        search_string = self.kwargs.get('search')
        list = search_string.split(sep=" ")
        # Running a filter with a reduced query 
        # lambda expression used to reduce a list of queries from Q 
        # into one from the list of strings
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
        userid = self.request.session['member_id']
        context['localUser'] = User.objects.get(user_id=userid)
        # self.reviews_list = 
        return context
    

class ReviewView(generic.FormView):
    model = Game
    form_class = ReviewForm
    template_name = "reviews/review.html"

    def form_valid(self, form):
        review = GameReview.objects.create(
            user_id=User.objects.get(user_id=self.request.session['member_id']),
            game_id=Game.objects.get(game_id=self.kwargs.get('pk')),
            review=form.cleaned_data['review'],
            score=form.cleaned_data['score'],
            publish_date=timezone.now()
        )
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        game = Game.objects.get(game_id=self.kwargs.get('pk'))
        return "/reviews/" + str(game.game_id) + "/game/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game'] = Game.objects.get(game_id=self.kwargs.get('pk'))
        userid = self.request.session['member_id']
        context['localUser'] = User.objects.get(user_id=userid)
        return context


def search(request):
    search_string = request.POST['searchString']
    return HttpResponseRedirect(reverse('reviews:searchresults', kwargs={'search':search_string}))


def registerLogin(request):
    try:
        user = User.objects.get(username=request.POST['username'])
    except (KeyError, User.DoesNotExist):
        newUser = User.objects.create(
            username= request.POST['username'],
            password= request.POST['password'],
            creation_date = timezone.now()
        )
        request.session['member_id'] = newUser.user_id
        return render(request, "reviews:home")
    else:
        m = User.objects.get(username=request.POST['username'])
    if m.password == request.POST['password']:
        request.session['member_id'] = m.user_id
        return HttpResponseRedirect(reverse("reviews:home"))
    else:
        return HttpResponseRedirect(reverse('reviews:register'))

def login(request):
    m = User.objects.get(username=request.POST['username'])
    if m.password == request.POST['password']:
        request.session['member_id'] = m.user_id
        return HttpResponseRedirect(reverse("reviews:home"), args=(m.user_id))
    else:
        return HttpResponseRedirect(reverse('reviews:register'))


def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('reviews:login'))


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
