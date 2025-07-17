from celery import shared_task
import random
from analytics.models import Task, TaskData
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail

@shared_task
def welcome_message(id):
    try:
        task = Task.objects.get(id=id)
        # Do your long-running logic here (e.g., send emails, update accounting)
        # ...
        message_choices = [
             'Thanks for choosing Northstar! Your task is now with an expert. Need to add more details or files? Just reply here - we will ensure your spreadsheets work perfectly!',
            'message two',
             'message three',
             'message four'
         ]
        description = random.choice(message_choices)
        TaskData.objects.create(
            task=task,
            description=description,
            is_auto_created=True,
            is_mod=True  # Assuming this field exists
        )
    except task.DoesNotExist:
        pass


@shared_task
def notification_message(id):
    try:
        item = TaskData.objects.get(id=id)
        email = item.task.user.email
        html_template = 'analytics/email/message.html'
        html_message = render_to_string(html_template)
        subject = 'New Message Received For Your Project'
        email_from = 'Northstar@northstar.com'
        recipient_list = [email]
        message = EmailMessage(subject, html_message,
                                email_from, recipient_list)
        message.content_subtype = 'html'
        message.send(fail_silently=True)
    except item.DoesNotExist:
        pass



@shared_task
def admin_message(id):
    try:
        item = TaskData.objects.get(id=id)
        html_template = 'analytics/email/message.html'
        html_message = render_to_string(html_template)
        subject = 'New client Message'
        email_from = 'northstar@northstar.com'
        recipient_list = 'bestessays001@gmail.com'
        message = EmailMessage(subject, html_message,
                                email_from, recipient_list)
        message.content_subtype = 'html'
        message.send(fail_silently=True)
    except item.DoesNotExist:
        pass


@shared_task
def welcome_email(email):
    html_template = 'analytics/email/signup.html'
    html_message = render_to_string(html_template)
    subject = 'Welcome to Northstar'
    email_from = 'Northstar@the-northstar.com'
    recipient_list = [email]
    
    message = EmailMessage(subject, html_message, email_from, recipient_list)
    message.content_subtype = 'html'
    message.send(fail_silently=True)