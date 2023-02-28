from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('userapp/contact/', ContactView.as_view(), name="contact"),
    path('userapp/about/', AboutView.as_view(), name="about"),
    path('userapp/joblist/', JobListView.as_view(), name="joblist"),
    path('userapp/postajob/', JobPostView.as_view(), name="postajob"),
    path('userapp/filteredjoblist/', FilterJobListView.as_view(), name="filterjobs"),
    path('userapp/jobdetail/<int:pk>/', JobDetailView.as_view(), name="jobdetail"),
    path('userapp/jobcategory/', JobCategoryView.as_view(), name="jobcategory"),
    path('userapp/testimonial/', TestimonialView.as_view(), name="testimonial"),
    path('userapp/404/', ErrorPageView.as_view(), name="404"),
    path('userapp/talentlist/', TalentListView.as_view(), name="talentlist"),
    path('userapp/filteredtalentlist/', FilterTalentListView.as_view(), name="filtertalents"),
    path('userapp/talentdetail/<int:pk>/', TalentDetailView.as_view(), name="talentdetail"),
    path('userapp/settings/<int:pk>/', SettingView.as_view(), name="settings"),
    path('userapp/login/', LoginView.as_view(), name="login"),
    path('userapp/logout/', LogoutView.as_view(), name="logout"),
    path('userapp/registration/', RegistrationView.as_view(), name="registration"),
    path('userapp/passwordchange/', ChangePasswordView.as_view(), name="passwordchange"),
    path('userapp/becomeworker/', BecomeWorkerView.as_view(), name="becomeworker"),
    path('userapp/updateworkerprofile/<int:pk>/', WorkerProfileUpdateView.as_view(), name="updateworkerprofile"),


]
