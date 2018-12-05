from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    creation_date = models.DateTimeField("creation date")

    def __str__(self):
        return "User: "+ user_id + " " + self.username

    def created_recently(self):
        return self.creation_date > timezone.now() - datetime.timedelta(days=1)


class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    publish_date = models.DateTimeField("publish_date")
    console = models.CharField(max_length=50)

    def __str__(self):
        return "Game: " + self.name + " | Console: " + self.console
    
    def published_recently(self):
        return self.publish_date > timezone.now() - datetime.timedelta(days=1)


class GameReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    score =  models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(5)
    ], default=0,
    )
    review = models.TextField()
    publish_date = models.DateTimeField("publish_date")

    def published_recently(self):
        return self.publish_date > timezone.now() - datetime.timedelta(days=1)
    
    def show_score(self):
        return str(score) + "/5" 