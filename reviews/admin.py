from django.contrib import admin
from .models import Game, GameReview, User
# Register your models here.
admin.site.register(User)
admin.site.register(Game)
admin.site.register(GameReview)