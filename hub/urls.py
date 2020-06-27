from django.urls import path
from . import views
urlpatterns = [
    path('', views.comingSoon, name='comingSoon'),
    path('dev', views.index, name='index'),
    path('dev/create', views.createProject, name='createProject'),
    path('dev/create/<int:projectID>', views.createProject, name='createProject'),
    path('dev/discovery', views.discovery, name='discovery'),
    path('dev/getParts', views.getParts, name='getParts'),
    path('dev/login', views.loginAndRegister, name='loginAndRegister'),
    path('dev/login/<slug:slug>', views.loginAndRegister, name='loginAndRegister'),
    path('dev/getCategories', views.getCategories, name='getCategories'),
    path('dev/project/<slug:slug>/', views.project, name='project'),
    path('dev/upvote', views.upvote, name='upvote'),
    path('dev/addComment', views.addComment, name='addComment'),
    path('dev/logout', views.logout, name='logout'),
    path('dev/profile', views.profile, name='profile'),
    path('dev/profile/<slug:username>', views.profile, name='profile'),
    path('dev/filterProjects', views.filterProjects, name='filterProjects'),
    path('dev/filterProjects/<slug:filter>', views.filterProjects, name='filterProjects'),
    path('dev/filterProjects/<slug:filter>/<int:num_of_results>', views.filterProjects, name='filterProjects'),
    path('dev/filterProjects/<slug:filter>/<int:num_of_results>/<int:page>', views.filterProjects, name='filterProjects'),
    path('dev/filterProjects/<slug:filter>/<int:num_of_results>/<int:page>/<slug:category>', views.filterProjects, name='filterProjects'),
    path('dev/contact', views.contact, name='contact'),
    path('dev/about', views.about, name='about'),
    path('dev/getProjects', views.getProjectsByParts, name='getProjects'),
    path('dev/forgotPassword', views.forgotPassword, name='forgotPassword'),
    path('dev/resetPassword', views.resetPassword, name='resetPassword')
]