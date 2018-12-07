from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class UserForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(),max_length=20)

class ReviewForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea, required=True)
    score = forms.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(5)
    ])
