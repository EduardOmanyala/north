from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from frontend import views as front_views

urlpatterns = [
    path('', front_views.frontEnd, name='home'),
    path('users/profile', front_views.profile2, name='profile'),
]




