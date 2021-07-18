from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import MyLoginView, MySignupView

app_name = 'accounts'
urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('signup/', MySignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout')
]
