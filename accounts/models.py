from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db import models

# Create your models here.
from django.views.generic import CreateView


class MySignupView(CreateView):

    form_class = UserCreationForm
    success_url = 'accounts:login'
    template_name = 'accounts/register.html'


class MyLoginView(LoginView):
     redirect_authenticated_user = True
     template_name = 'accounts/login.html'
