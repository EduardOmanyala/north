from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from analytics.models import Task, TaskData, TaskNotifications, AdminNotifications, Message, MessageNotifications, AdminMessageNotifications
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
import random
from analytics.scheduler import  welcome_message, notification_message, admin_message

@receiver(post_save, sender=TaskData)
def create_task_notification(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.is_mod:
        message = (
            "Submission made for your project"
            if instance.is_answer else
            "New Message received on your project"
        )
        TaskNotifications.objects.create(task=instance.task, message=message, user=instance.task.user)
        #notification_message.apply_async(args=[instance.id], countdown=60)   
  
    else:
        AdminNotifications.objects.create(
            task=instance.task,
            message="New task message received"
        )
        #admin_message.apply_async(args=[instance.id], countdown=60)  
       
    



@receiver(pre_save, sender=Task)
def cache_previous_paid_value(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous = Task.objects.get(pk=instance.pk)
            instance._previous_paid = previous.paid
        except Task.DoesNotExist:
            instance._previous_paid = None
    else:
        instance._previous_paid = None

# --- Post save logic for create and paid=True ---
@receiver(post_save, sender=Task)
def create_admin_notification(sender, instance, created, **kwargs):
    if created:
        AdminNotifications.objects.create(
            task=instance,
            message="A new task has been created."
        )
        #admin_message.apply_async(args=[instance.id], countdown=60) 
    elif not created and not getattr(instance, '_previous_paid', False) and instance.paid:
        AdminNotifications.objects.create(
            task=instance,
            message="A task has been marked as paid."
        )
      
        



@receiver(post_save, sender=Message)
def message_notifications(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.isAdmin:
        message ="You have a new message"
        MessageNotifications.objects.create(user=instance.user, message=message)
        #notification_message.apply_async(args=[instance.id], countdown=60)   
      
        

    else:
        AdminMessageNotifications.objects.create(
            user=instance.user,
            message="New client message received"
        )
        #admin_message.apply_async(args=[instance.id], countdown=60) 
      

