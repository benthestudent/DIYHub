from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.createProject, name='createProject'),
    path('getParts', views.getParts, name='getParts'),
    path('login', views.loginAndRegister, name='loginAndRegister'),
    path('login/<slug:slug>', views.loginAndRegister, name='loginAndRegister'),
    path('getCategories', views.getCategories, name='getCategories'),
    path('project/<slug:slug>/', views.project, name='project'),
    path('upvote', views.upvote, name='upvote'),
    path('addComment', views.addComment, name='addComment'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile')
]