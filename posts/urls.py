from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.HomeView, name="home"),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('all_users/',views.all_user,name="all_users"),
    path('follow/<str:username>/',views.follow,name="follow-unfollow"),
    path('question/<slug:slug>',views.detailedquestion,name="question-detail"),
    path('askquestion/',views.askquestion,name="ask-question"),
    path('addanswer/<slug:slug>/',views.addAnswer,name="add-answer"),
    path('upvoteanswer/<int:pk>/',views.upvote,name="like-answer"),
    path('downvoteanswer/<int:pk>/', views.downvote, name="dislike-answer"),
    path('delete_post/<int:pk>/', views.delete_post, name="delete_post"),

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)