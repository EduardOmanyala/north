# Generated by Django 4.2.6 on 2025-03-21 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_blog_title2_alter_blog_slug_alter_blog_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
