from django.contrib import admin
from django.forms import forms, Textarea
from django.db import models
from core.models import Blog, Category, RequestCount






# Register your models here.
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(RequestCount)
