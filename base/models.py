# ------import------
from django.db import models
from django.contrib.auth.models import User

class FacebookUsers(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    email = models.CharField(max_length=40,null=True)
    password = models.CharField(max_length=40,null=True)
 

    def __str__(self):
        return f'Profile for user {self.user.username}'

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    post = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'post for user {self.user.username}'