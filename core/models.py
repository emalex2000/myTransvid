from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Register(models.Model):
    username: models.CharField(max_length=2000, null=True)
    email: models.CharField(max_length=2000, null=True)
    password: models.CharField(max_length=2000, null=True)

    def __str__(self):
        return self.name
# Create your models here.

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_title = models.CharField(max_length=300, null=True)
    video_link = models.URLField(null=True)
    created_in = models.DateTimeField(auto_now_add=True)
    generated_content = models.TextField(null=True)

    def __str__(self):
        return self.youtube_title