from django import forms

class UserForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(),max_length=20)

class ReviewForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea, required=True)