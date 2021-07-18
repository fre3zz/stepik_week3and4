from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView


class MySignupView(CreateView):

    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/register.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'
