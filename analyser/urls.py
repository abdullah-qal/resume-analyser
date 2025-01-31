from django.urls import path 
from . import views 

urlpatterns = [ 
    path('', views.index, name='index'),
    path('upload_resume', views.upload_resume, name='upload_resume'),
    path('parse_job_posting', views.parse_job_posting, name='parse_job_posting')
]