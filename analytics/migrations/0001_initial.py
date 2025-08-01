# Generated by Django 4.2.6 on 2025-05-24 18:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadline', models.DateTimeField()),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('description', tinymce.models.HTMLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('paid', models.BooleanField(default=False)),
                ('complete', models.BooleanField(default=False)),
                ('cancelled', models.BooleanField(default=False)),
                ('time_paid', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Tasks',
            },
        ),
        migrations.CreateModel(
            name='TaskData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instructions', tinymce.models.HTMLField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='TaskFiles/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_mod', models.BooleanField(default=False)),
                ('is_answer', models.BooleanField(default=False)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analytics.task')),
            ],
            options={
                'verbose_name_plural': 'Tasks',
            },
        ),
    ]
