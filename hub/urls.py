from django.urls import path, re_path
from . import views
urlpatterns = [
    path('', views.comingSoon, name='comingSoon'),
    path('dev', views.index, name='index'),
    path('dev/create', views.createProject, name='createProject'),
    path('dev/create/<int:projectID>', views.createProject, name='createProject'),
    path('dev/link', views.linkProject, name='linkProject'),
    path('dev/link/<int:projectID>', views.linkProject, name='linkProject'),
    path('dev/discovery', views.discovery, name='discovery'),
    path('dev/getParts', views.getParts, name='getParts'),
    path('dev/login', views.loginAndRegister, name='loginAndRegister'),
    path('dev/login/<slug:slug>', views.loginAndRegister, name='loginAndRegister'),
    path('dev/getCategories', views.getCategories, name='getCategories'),
    path('dev/project/<slug:slug>/', views.project, name='project'),
    path('dev/project/external/', views.project, name='external_project'),
    path('dev/upvote', views.upvote, name='upvote'),
    path('dev/addComment', views.addComment, name='addComment'),
    path('dev/logout', views.logout, name='logout'),
    path('dev/profile', views.profile, name='profile'),
    path('dev/profile/<slug:username>', views.profile, name='profile'),
    path('dev/filterProjects', views.filterProjects, name='filterProjects'),
    path('dev/filterProjects/<slug:filter>', views.filterProjects, name='filterProjects'),
    path('dev/filterProjects/<slug:filter>/<int:num_of_results>', views.filterProjects, name='filterProjects'),
    path('dev/filterProjects/<slug:filter>/<int:userID>/<int:num_of_results>', views.filterProjects, name='filterProjects'),
    path('dev/filterProjects/<slug:filter>/<int:num_of_results>/<int:page>', views.filterProjects, name='filterProjects'),
    path('dev/filterProjects/<slug:filter>/<int:num_of_results>/<int:page>/<slug:category>', views.filterProjects, name='filterProjects'),
    path('dev/contact', views.contact, name='contact'),
    path('dev/about', views.about, name='about'),
    path('dev/getProjects', views.getProjectsByParts, name='getProjects'),
    path('dev/forgotPassword', views.forgotPassword, name='forgotPassword'),
    re_path('dev/resetPassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})', views.resetPassword, name='resetPassword_confirm'),
    path('dev/resetPassword/done', views.resetPassword, name='resetPassword_complete')
]