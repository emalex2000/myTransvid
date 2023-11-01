# Generated by Django 4.2.5 on 2023-09-23 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_blogpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='youtube_title',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='generated_content',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='video_link',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='video_title',
            field=models.CharField(max_length=300, null=True),
        ),
    ]