from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.createProject, name='createProject'),
    path('discovery', views.discovery, name='discovery'),
    path('getParts', views.getParts, name='getParts'),
    path('login', views.loginAndRegister, name='loginAndRegister'),
    path('login/<slug:slug>', views.loginAndRegister, name='loginAndRegister'),
    path('getCategories', views.getCategories, name='getCategories'),
    path('project/<slug:slug>/', views.project, name='project'),
    path('upvote', views.upvote, name='upvote'),
    path('addComment', views.addComment, name='addComment'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('profile/<slug:username>', views.profile, name='profile'),
    path('filterProjects', views.filterProjects, name='filterProjects'),
    path('filterProjects/<slug:filter>', views.filterProjects, name='filterProjects'),
    path('filterProjects/<slug:filter>/<int:num_of_results>', views.filterProjects, name='filterProjects'),
    path('filterProjects/<slug:filter>/<int:num_of_results>/<int:page>', views.filterProjects, name='filterProjects'),
    path('filterProjects/<slug:filter>/<int:num_of_results>/<int:page>/<slug:category>', views.filterProjects, name='filterProjects'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('getProjects', views.getProjectsByParts, name='getProjects')
]