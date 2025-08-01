from django.db import models
from custom_user.models import User
from django.utils.text import slugify
from tinymce.models import HTMLField
import os
from datetime import timedelta
from django.utils import timezone
import random


# Create your models here.



TYPE_CHOICES = (
    ('Excel','Excel'),
    ('SPSS', 'SPSS'),
    ('Python','Python'),
    ('Machine Learning','Machine Learning'),
    ('Matlab','Matlab'),
    ('R','R'),
    ('Tableau','Tableau'),
    ('React','React'),
    ('Django','Django'),
    ('Vue','Vue'),
)


PROGRESS_CHOICES = [
        (30, '30'),
        (40, '40'),
        (50, '50'),
        (60, '60'),
        (70, '70'),
        (80, '80'),
        (90, '90'),
    ]


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    title = models.CharField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=230, null=True, blank=True, unique=False)
    type = models.CharField(max_length=200, choices=TYPE_CHOICES, default='Excel')
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    completion_date = models.DateTimeField(blank=True, null=True)
    cancelled = models.BooleanField(default=False)
    time_paid = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Tasks"

    def save(self, *args, **kwargs):
        #assign slug
        self.slug = slugify(self.title)
        #assign image
        if not self.image_path:
            # List of available image filenames
            image_choices = [
                'analytics/imgs/person.png',
                'analytics/imgs/person2.jpg',
                'analytics/imgs/person3.jpg',
                'analytics/imgs/person4.jpg',
                'analytics/imgs/person5.jpg',
                'analytics/imgs/person6.jpg',
                'analytics/imgs/person7.jpg',
            ]
            self.image_path = random.choice(image_choices)
        super().save(*args, **kwargs)


    def image_url(self):
        from django.templatetags.static import static
        return static(self.image_path)
    
    
    @property
    def default_price(self):
        price_map = {
            'Excel': 39,
            'SPSS': 42,
            'Python': 49,
            'Machine Learning': 79,
            'Matlab': 62,
            'R': 52,
            'Tableau': 130,
            'React':250,
            'Django':200,
            'Vue':200,
        }
        return price_map.get(self.type, 0)
    @property
    def time_remaining_pretty(self):
        delta = self.deadline - timezone.now()
        if delta.total_seconds() < 0:
            return "Past due"
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{days}d {hours}h {minutes}m"

    @property
    def time_progress_percent(self):
        now = timezone.now()
        total_duration = self.deadline - self.created_at
        time_spent = now - self.created_at

        # If deadline has already passed
        if now >= self.deadline:
            return 100
        # If task has not started yet (somehow)
        if time_spent.total_seconds() < 0:
            return 0
        if self.complete:
            return 100
        else:
            progress = (time_spent.total_seconds() / total_duration.total_seconds()) * 100
            return int(progress)


class TaskData(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = HTMLField(blank=True, null=True)
    created_at =  models.DateTimeField(auto_now_add=True)
    is_mod = models.BooleanField(default=False)
    is_answer = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    adminRead = models.BooleanField(default=False)
    is_auto_created = models.BooleanField(default=False)
    is_status = models.BooleanField(default=False)
    progress = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "TaskDatas"

    def __str__(self):
        return str(self.task.title)
    

class TaskFiles(models.Model):
    taskdata = models.ForeignKey(TaskData, on_delete=models.CASCADE)
    file = models.FileField(upload_to='TaskFiles/', blank=True, null=True)
    created_at =  models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "TaskFiles"

    def __str__(self):
        return str(self.taskdata.task)
    @property
    def filename(self):
        return os.path.basename(self.file.name)

    @property
    def css_class(self):
        name, extension = os.path.splitext(self.file.name)
        if extension == '.pdf':
            return 'pdf'
        elif extension == '.docx':
            return 'word'
        elif extension == '.doc':
            return 'word'
        elif extension == '.xlsx':
            return 'excel'
        elif extension == '.pptx':
            return 'ppt'
        else:
            return 'other'  
        
class TaskNotifications(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    message = models.CharField(max_length=500, blank=True, null=True)
    created_at =  models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = "TaskNotifications"

    def __str__(self):
        return str(self.task.title)
    

class AdminNotifications(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    message = models.CharField(max_length=500, blank=True, null=True)
    created_at =  models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "AdminNotifications"

    def __str__(self):
        return str(self.task.title)
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = HTMLField(blank=True, null=True)
    isAdmin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)



class MessageNotifications(models.Model):
    message = models.CharField(max_length=500, blank=True, null=True)
    created_at =  models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = "MessageNotifications"

    

class AdminMessageNotifications(models.Model):
    message = models.CharField(max_length=500, blank=True, null=True)
    created_at =  models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = "AdminMessageNotifications"

  