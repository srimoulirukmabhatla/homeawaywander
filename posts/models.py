from django.db import models
from django.contrib.auth.models import  User
# Create your models here.
from django.db.models.signals import post_save,post_delete
from notifications.models import Notification
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

class Question(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.CharField(max_length=100)
    published_date=models.DateTimeField(auto_now_add=True)
    ques_image = models.ImageField(upload_to="images/",default="defaultt.png", null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=100,default="Some Question")
    tags = TaggableManager()
    def __str__(self):
        return str(self.body)


class Answer(models.Model):
    question=models.ForeignKey(Question,related_name="answers",on_delete=models.CASCADE)
    body=RichTextField(blank=True,null=True)
    published_date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    publisher=models.ForeignKey(User,on_delete=models.CASCADE)
    upvotes=models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    def user_answered(sender,instance,*args,**kwargs):
        if kwargs['created']:
            answer=instance
            senderr=answer.publisher
            Notification.objects.create(answer=answer,senderr=senderr,user=answer.question.author,notification_type=3)
    def __str__(self):
        return str(self.body)
#for answers added
post_save.connect(Answer.user_answered,sender=Answer)
class Upvote(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_upvote")
    ans=models.ForeignKey(Answer,on_delete=models.CASCADE,related_name="ans_upvote")
    def user_upvoted(sender,instance,*args,**kwargs):
        if kwargs['created']:
            upvote=instance
            ans=upvote.ans
            senderr=upvote.user
            Notification.objects.create(answer=ans,senderr=senderr,user=ans.publisher,notification_type=1)

post_save.connect(Upvote.user_upvoted,sender=Upvote)
class Downvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_downvote")
    ans = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="ans_downvote")
    def user_downvoted(sender,instance,*args,**kwargs):
        if kwargs['created']:
            downvote=instance
            ans=downvote.ans
            senderr=downvote.user
            Notification.objects.create(answer=ans,senderr=senderr,user=ans.publisher,notification_type=2)
post_save.connect(Downvote.user_downvoted,sender=Downvote)



