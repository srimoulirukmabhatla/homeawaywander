from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.
from django.http import HttpResponseRedirect
import json
from django.urls import reverse
from django.views.generic import ListView,DetailView
from .forms import  *
from user.models import *
from .models import *
from django.db.models import Q
from notifications.models import *
from taggit.models import Tag
from django.template.defaultfilters import slugify
import datetime
def homepage(request):
    notifications=Notification.objects.filter(user=request.user)
    context={'notifications': notifications}
    return render(request,'base.html',context=context)

def all_user(request):
    logged_user=request.user
    notifications=Notification.objects.filter(user=request.user)
    users=User.objects.all()
    context={'users':users,'notifications': notifications}
    return render(request,'all_users.html',context)
def follow(request, username):


    main_user = request.user
    to_follow = User.objects.get(username = username)

    #check if already following
    following = Follow.objects.filter(following=main_user, follower=to_follow)
    is_following = True if following else False

    if is_following:
        following.delete()
        is_following = False

    else:
        follow_obj=Follow(following=main_user,follower=to_follow)
        follow_obj.save()
        is_following = True

    resp = {
        "following" : is_following,
    }
    return redirect('profile-visit',username=to_follow)

def delete_post(request, pk):
    ques=Question.objects.get(id=pk)
    ques.delete()
    return redirect('home')

def HomeView(request):
    if request.user.is_authenticated:
        questions=Question.objects.all().order_by('-published_date')
        notifications=Notification.objects.filter(user=request.user)
        context={'questions':questions,'notifications': notifications}
        template_name = 'home.html'
        return render(request,'home.html',context=context)
    else:
        return redirect('login')

def detailedquestion(request,slug):
    if request.user.is_authenticated:
        user_visit=request.user
        notifications=Notification.objects.filter(user=request.user)

        quest=get_object_or_404(Question,slug=slug)
        quest_user=quest.author
        answrs=Answer.objects.filter(question=quest)
        upvotes=Upvote.objects.all()
        context={'quest':quest,'answrs':answrs,'user_visit':user_visit,'upvotes':upvotes,'notifications': notifications,'quest_user':quest_user}
        return render(request,'detailed.html',context=context)
    else:
        return redirect('login')
def askquestion(request):
    if request.user.is_authenticated:
        user_asking=request.user
        form = AskQuestionForm(request.POST, request.FILES)
        notifications=Notification.objects.filter(user=request.user)
        if request.method=='POST':
            post=form.save(commit=False)
            post.slug=slugify(str(post.body)+("_")+str(user_asking)+("_")+str(datetime.datetime.now()))
            post.author=user_asking
            post.save()
            form.save_m2m()
            return redirect('home')
        context={'form':form,'notifications':notifications}
        return render(request,'askquestion.html',context=context)
    else:
        return redirect('login')
def addAnswer(request,slug):
    if request.user.is_authenticated:
        ques=get_object_or_404(Question,slug=slug)
        user_visit=request.user
        form=AddAnswer(request.POST)
        notifications=Notification.objects.filter(user=request.user)

        if request.method=='POST':
            post=form.save(commit=False)
            post.publisher=user_visit
            post.question=ques
            post.save()
            return redirect('question-detail' ,slug=slug)
        context={'form':form,'notifications':notifications}
        return render(request,'addanswer.html',context=context)
    else:
        return redirect('login')
def upvote(request,pk):
    if request.user.is_authenticated:
        ans=Answer.objects.get(id=pk)
        quest_id=ans.question.slug
        curr_upvotes=ans.upvotes
        curr_downvotes=ans.downvotes
        dv1=Downvote.objects.filter(user=request.user,ans=ans).count()
        uv3=Upvote.objects.filter(user=request.user,ans=ans).count()
        if not uv3: #agar upvote nhi kiya hua
            if not dv1: #agar downvo
                curr_upvotes+=1
                ans.upvotes = curr_upvotes
                ans.downvotes = curr_downvotes
                ans.save()
            else:
                Downvote.objects.filter(user=request.user,ans=ans).delete()
                curr_upvotes+=1
                curr_downvotes-=1
                ans.upvotes = curr_upvotes
                ans.downvotes = curr_downvotes
                ans.save()
        uv1 = Upvote.objects.create(user=request.user, ans=ans)
        uv1.save()
        return HttpResponseRedirect(reverse('question-detail',args=[str(quest_id)]))
    else:
        return redirect('login')
def downvote(request,pk):
    if request.user.is_authenticated:
        ans=Answer.objects.get(id=pk)
        quest_id=ans.question.slug

        curr_upvotes=ans.upvotes
        curr_downvotes=ans.downvotes
        # ans.upvotes.remove(request.user)
        # ans.downvotes.add(request.user)
        uv2=Upvote.objects.filter(user=request.user,ans=ans).count()
        dv3=Downvote.objects.filter(user=request.user,ans=ans).count()
        if not dv3:
            #agar upvote nhi kiya hua
            if not uv2:
                dv2=Downvote.objects.create(user=request.user,ans=ans)
                dv2.save()
                curr_downvotes+=1
                ans.upvotes = curr_upvotes
                ans.downvotes = curr_downvotes
                ans.save()
            else:
                Upvote.objects.filter(user=request.user,ans=ans).delete()
                dv2 = Downvote.objects.create(user=request.user, ans=ans)
                dv2.save()
                curr_downvotes+=1
                curr_upvotes-=1
                ans.upvotes = curr_upvotes
                ans.downvotes = curr_downvotes
                ans.save()
        return HttpResponseRedirect(reverse('question-detail',args=[str(quest_id)]))
    else:
        return redirect('login')



class SearchResultsView(ListView):
    model = Question
    template_name = 'search_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')

        object_list=Question.objects.filter(
                    Q(body__icontains=query)
            )
        return object_list


