from django.db import models
from custom_user.models import User
from tinymce.models import HTMLField
import string  
import random 
from django.utils.text import slugify


TYPE_CHOICES = (
    ('Main','Main'),
    ('Ordinary', 'Ordinary'),
    ('Featured','Featured'),
)

class Category(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='category-images/', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        #self.slug = self.generate_slug()
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Blog(models.Model):
    type = models.CharField(max_length=200, choices=TYPE_CHOICES, default='Ordinary')
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post-images/', blank=True, null=True)
    main = HTMLField(blank=True, null=True)
    slug = models.SlugField(null=True, blank=True, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Blogs'

    def save(self, *args, **kwargs):
        #self.slug = self.generate_slug()
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    



class RequestCount(models.Model):
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def increment(cls):
        obj, created = cls.objects.get_or_create(id=1)
        obj.count += 1
        obj.save()

    