from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from frontend import views as front_views

urlpatterns = [
    path('', front_views.frontEnd, name='home'),
    path('users/profile', front_views.profile2, name='profile'),
    path('index/test', front_views.frontEnd2, name='indextest'),
    path('privacy-policy', front_views.privacyPolicy, name='p-policy'),
    path('terms-of-service', front_views.termsOfService, name='t-serve'),
    path('subscribe/success', front_views.subscribe_view, name='subscribe-view'),
]




