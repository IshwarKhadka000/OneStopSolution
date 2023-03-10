from django.urls import path
from .views import *

urlpatterns = [

    # dashboard
    path('', IndexView.as_view(), name="dashboard"),
    

    # services
    path('service_list/', ServiceListView.as_view(), name="service_list"),
    path('add_service/', AddServiceView.as_view(), name="add_service"),
    path('edit_service/<int:pk>', EditServiceView.as_view(), name="edit_service"),
    path('delete_service/<int:pk>', DeleteServiceView.as_view(), name="delete_service"),

    # skills
    path('skill_list/', SkillListView.as_view(), name="skill_list"),
    path('add_skill/', AddSkillView.as_view(), name="add_skill"),
    path('edit_skill/<int:pk>/', EditSkillView.as_view(), name="edit_skill"),
    path('delete_skill/<int:pk>/', DeleteSkillView.as_view(), name="delete_skill"),

    # users
    
    path('user_list/', ClientListView.as_view(), name="user_list"),

    # workers
    path('worker_list/', WorkerListView.as_view(), name="worker_list"),
    path('worker_detail/<int:pk>/', WorkerDetailView.as_view(), name="worker_detail"),

    # jobs
    path('job_list/', JobListView.as_view(), name="job_list"),
    path('job_detail/<int:pk>/', JobDetailView.as_view(), name="job_detail"),

    # queries
    path('query_list/', QueryListView.as_view(), name="query_list"),
    path('query_detail/<int:pk>/', QueryDetailView.as_view(), name="query_detail"),
    path('delete_query/<int:pk>', DeleteQueryView.as_view(), name="delete_query"),


]
