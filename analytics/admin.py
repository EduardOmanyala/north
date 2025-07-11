from django.contrib import admin
from analytics.models import Task, TaskData, TaskFiles, AdminMessageNotifications, MessageNotifications, TaskNotifications, AdminNotifications

# Register your models here.
admin.site.register(Task)
admin.site.register(TaskData)
admin.site.register(TaskFiles)
admin.site.register(AdminMessageNotifications)
admin.site.register(MessageNotifications)
admin.site.register(TaskNotifications)
admin.site.register(AdminNotifications)
