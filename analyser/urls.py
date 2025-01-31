from django.urls import path 
from . import views 

urlpatterns = [ 
    path('', views.index, name='index'),
    path('match_requirements', views.match_requirements, name='match_requirements')
]