
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    profile_pic = models.ImageField(default="defaultt.png", null=True, blank=True)
    def __str__(self):
    	return f'{self.user.username}'
class Follow(models.Model):
    following = models.ForeignKey(User, related_name="who_follows",on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name="who_is_followed",on_delete=models.CASCADE)
    follow_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.following.username}'