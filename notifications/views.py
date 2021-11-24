from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import *
import json
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.urls import reverse

def shownotifications(request):
    user=request.user
    notifications=Notification.objects.filter(user=user).order_by('-date')
    my_dict={'notifications':notifications}
    return render(request,'notifications.html',context=my_dict)


def clearnotification(request,pk):
    noti=Notification.objects.get(id=pk)
    noti.delete()
    return HttpResponseRedirect(reverse('show-notifications'))

def clearall(request):
    noti=Notification.objects.filter(user=request.user)
    noti.delete()
    return HttpResponseRedirect(reverse('show-notifications'))

