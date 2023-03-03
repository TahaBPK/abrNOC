from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# This is the form I make to register new users to my system

class NewUserForm(UserCreationForm):
    class Meta:
        username = forms.CharField(max_length=100, required=True)
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user
