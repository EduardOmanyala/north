from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from core import views as core_views

urlpatterns = [
    path('', core_views.home, name='home'),

    path('post', core_views.post, name='post'),
    path('<str:slug>/<int:id>', core_views.post_detail, name='post-detail'),
    path('update/<str:slug>/<int:id>', core_views.post_update, name='post-update'),
    path('delete/post/<int:id>', core_views.delete_post, name='post-delete'),

    path('create/new/category', core_views.categoryCreate, name='category-create'),
    path('categories', core_views.categories, name='categories'),
    path('category/update/<int:id>/<str:slug>', core_views.post_update, name='cat-update'),
    path('category/posts/<int:id>/<str:slug>', core_views.categoryPosts, name='cat-posts'),

    path('user/dashboard', core_views.adminDashBoard, name='admin-dashboard'),
    path('search/', core_views.search, name='search'),
    path('subscribe/', core_views.subscribe_view, name='subscribe'),
   
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('register/', core_views.register, name='register'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="core/reset_password_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="core/password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="core/password_reset_done.html"), name='password_reset_complete'),
    
    path('profile', core_views.profile, name='profile'),
    path('about', core_views.about, name='about'),
    path('mailtest', core_views.mailtest1, name='mailtest'),
    path('welcomemail', core_views.welcomemail, name='welcomemail'),
    path('contactus', core_views.contactus, name='contactus'),
   
]



