# Generated by Django 4.2.6 on 2025-03-21 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_blog_new_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='new_title',
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
