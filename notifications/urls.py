from django.urls import path
from notifications.views import shownotifications,clearnotification,clearall


urlpatterns = [
   	path('', shownotifications, name='show-notifications'),
	path('clearnotifications/<int:pk>/', clearnotification, name='clear-notification'),
	path('clearall/',clearall,name='clear-all'),

]