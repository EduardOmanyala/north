from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from analytics import views as a_views

urlpatterns = [
    path('', a_views.homePage, name='home-page'),
    path('create/task/data', a_views.create_task, name='task-create'),
    path('projects/<int:id>/<str:slug>/', a_views.task_detail, name='task-info'),
    path('manage/<int:id>/<str:slug>/', a_views.task_detailAdmin, name='task-info-admin'),
    path('dashboard', a_views.task_listView, name='task-listview'),
    path('manage/dashboard', a_views.task_listViewAdmin, name='task-listview-admin'),
    path('checkout/<int:id>/', a_views.task_checkout, name='task-checkout'),
    path('base', a_views.BaseTest, name='base'),

    path('subjects/<str:type>/', a_views.subjectCategories, name='subjectCategories'),
    path('subjects/<str:type>/', a_views.subjectCategoriesAdmin, name='subjectCategories-admin'),
    path('project/status/<str:status>/', a_views.completeOrNot, name='completeornot'),

    path('ajax/notifications/', a_views.fetch_notifications, name='fetch_notifications'),
    path('notifications/mark-read/', a_views.mark_notifications_read, name='mark-notifications-read'),
    path('staff/ajax/notifications/', a_views.admin_fetch_notifications, name='admin_fetch_notifications'),
    path('staff/notifications/mark-read/', a_views.admin_mark_notifications_read, name='admin-mark-notifications'),

    path('messages/<int:m_user>/', a_views.getMessage, name='admin-user-messages'),
    path('post/messages/', a_views.newMessage, name='user-messages'),
    path('all/messages/', a_views.listMessages, name='all-messages'),

    path('ajax/messages/', a_views.admin_fetch_messages, name='admin_fetch_messages'),
    path('messages/mark-read/', a_views.admin_mark_messages_read, name='admin-messages-read'),
    path('ajax/updates/messages/', a_views.user_fetch_messages, name='user_fetch_messages'),
    path('messages/mark-read/', a_views.mark_messages_read, name='users-mark-notifications-read'),

    path('howitworks/', a_views.howItWorks, name='howitworks'),
]


