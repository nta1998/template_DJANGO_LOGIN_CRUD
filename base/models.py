# ------import------
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL,null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(default='/profile_pics.png', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    post = models.TextField(max_length=500, blank=True)
    pic = models.ImageField(default='/profile_pics.png', blank=True)

    def __str__(self):
        return f'post for user {self.user.username}'