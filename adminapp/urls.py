from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [

    # login
    path('adminapp/dashboard', login_required(AdminDashboardView.as_view(), login_url="adminlogin"), name='dashboard'),
    path('', AdminLogin.as_view(), name='adminlogin'),
    path('adminlogout/', AdminLogin.logout_view, name='adminlogout'),
    # services
    path('service_list/', login_required(ServiceListView.as_view()), name="service_list"),
    path('add_service/', AddServiceView.as_view(), name="add_service"),
    path('edit_service/<int:pk>', EditServiceView.as_view(), name="edit_service"),
    path('delete_service/<int:pk>', DeleteServiceView.as_view(), name="delete_service"),

    # skills
    path('skill_list/', login_required(SkillListView.as_view(), login_url="adminlogin"), name="skill_list"),
    path('add_skill/', login_required(AddSkillView.as_view(), login_url="adminlogin"), name="add_skill"),
    path('edit_skill/<int:pk>/', login_required(EditSkillView.as_view(), login_url="admin_login"), name="edit_skill"),
    path('delete_skill/<int:pk>/', login_required(DeleteSkillView.as_view(), login_url="adminlogin"), name="delete_skill"),

    # users
    path('user_list/', login_required(ClientListView.as_view(), login_url="admin_login"), name="user_list"),

    # workers
    path('worker_list/', login_required(WorkerListView.as_view(), login_url="admin_login"), name="worker_list"),
    path('worker_detail/<int:pk>/', login_required(WorkerDetailView.as_view(),login_url="admin_login"),  name="worker_detail"),
    path('edit_worker_status/<int:pk>/', login_required(EditWorkerStatusView.as_view(),login_url="admin_login"),  name="edit_worker_status"),

    # jobs
    path('job_list/', login_required(JobListView.as_view(), login_url="admin_login"), name="job_list"),
    path('job_detail/<int:pk>/', login_required(JobDetailView.as_view(),login_url="admin_login"),  name="job_detail"),

    # queries
    path('query_list/', login_required(QueryListView.as_view(),login_url="admin_login"),  name="query_list"),
    path('query_detail/<int:pk>/', login_required(QueryDetailView.as_view(),login_url="admin_login"),  name="query_detail"),
    path('delete_query/<int:pk>', login_required(DeleteQueryView.as_view(),login_url="admin_login"),  name="delete_query"),

    #status
    path('status_list', login_required(StatusListView.as_view(),login_url="admin_login"),  name="status_list"),
    path('add_status/', login_required(AddStatusView.as_view(), login_url="admin_login"),  name="add_status"),
    path('edit_status/<int:pk>/',login_required( EditStatusView.as_view(),login_url="admin_login"),  name="edit_status"),
    path('delete_status/<int:pk>/', login_required(DeleteStatusView.as_view(),login_url="admin_login"),  name="delete_status"),
]
