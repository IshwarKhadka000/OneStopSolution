from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('about/', AboutView.as_view(), name="about"),
    path('joblist/', JobListView.as_view(), name="joblist"),
    path('jobdetail/', JobDetailView.as_view(), name="jobdetail"),
    path('jobcategory/', JobCategoryView.as_view(), name="jobcategory"),
    path('testimonial/', TestimonialView.as_view(), name="testimonial"),
    path('404/', ErrorPageView.as_view(), name="404"),
    path('talentlist/', TalentListView.as_view(), name="talentlist"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('registration/', RegistrationView.as_view(), name="registration"),
    path('passwordchange/', ChangePasswordView.as_view(), name="passwordchange"),
    path('becomeworker/', BecomeWorkerView.as_view(), name="becomeworker"),
]
