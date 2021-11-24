from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Notification(models.Model):
    NOTIFICATION_TYPES=((1,'Upvote'),(2,'Downvote'),(3,'Answered'))
    answer=models.ForeignKey('posts.Answer',on_delete=models.CASCADE,related_name="noti_ans",blank=True,null=True)
    senderr=models.ForeignKey(User,on_delete=models.CASCADE,related_name="noti_from_user")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="not_to_user")
    notification_type=models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview=models.CharField(max_length=100,blank=True)
    date=models.DateTimeField(auto_now_add=True)
    is_seen=models.BooleanField(default=False)
    def __str__(self):
        return str(self.senderr)
