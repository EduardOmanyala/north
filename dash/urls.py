from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from dash import views as dash_views

urlpatterns = [
    path('dash/main', dash_views.dashMain, name='dash-main'),
    path('dash/base', dash_views.dashBase, name='dash-base'),
    path('myprojects/<int:id>/<str:slug>/', dash_views.task_detail, name='taskDetail'),
    path('pesapal/token/', dash_views.get_pesapal_token, name='pesapal_token'),
    path('pesapal/register-ipn/', dash_views.register_ipn, name='register_ipn'),
]



