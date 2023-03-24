from django.urls import path
from .views import *

urlpatterns = [
    # home page
    path('', IndexView.as_view(),
         name="index"),
    # contact us
    path('userapp/contact/', ContactView.as_view(),
         name="contact"),
    # about us
    path('userapp/about/', AboutView.as_view(),
         name="about"),
    # List of jobs
    path('userapp/joblist/', JobListView.as_view(),
         name="joblist"),
    # Posting a new job
    path('userapp/postajob/', login_required(JobPostView.as_view()),
         name="postajob"),
    # filtered list of jobs
    path('userapp/filteredjoblist/', FilterJobListView.as_view(),
         name="filterjobs"),
    # list of jobs based on category
    path('userapp/service/<int:service>/jobs/', CategoryJobListView.as_view(),
         name="category_jobs"),
    # Detail of a job
    path('userapp/jobdetail/<int:pk>/', JobDetailView.as_view(),
         name="jobdetail"),
    # Category list
    path('userapp/jobcategory/', JobCategoryView.as_view(),
         name="jobcategory"),
    # Testimonial Template view
    path('userapp/testimonial/', TestimonialView.as_view(),
         name="testimonial"),
    # Error template view
    path('userapp/404/', ErrorPageView.as_view(),
         name="404"),
    # List of all talents
    path('userapp/talentlist/', TalentListView.as_view(),
         name="talentlist"),
    # List of filtered talents
    path('userapp/filteredtalentlist/', FilterTalentListView.as_view(),
         name="filtertalents"),
    # Detail page of a talent
    path('userapp/talentdetail/<int:pk>/', TalentDetailView.as_view(),
         name="talentdetail"),
    # login
    path('userapp/login/', LoginView.as_view(),
         name="login"),
    # logout
    path('userapp/logout/', login_required(LogoutView.as_view()),
         name="logout"),
    # Registration
    path('userapp/registration/', RegistrationView.as_view(),
         name="registration"),
    # Change password
    path('userapp/passwordchange/', login_required(ChangePasswordView.as_view()),
         name="passwordchange"),
    # Worker profile creation
    path('userapp/becomeworker/', login_required(BecomeWorkerView.as_view()),
         name="becomeworker"),
    # Apply to a job
    path('userapp/applytoajob/<int:jobid>', JobProposalCreateView.as_view(),
         name="applytoajob"),
    # Newsletter subscription template view
    path('userapp/newsletter/', NewsLetterSubscribeView.as_view(),
         name="newsletter"),

    # worker profile
    # profile details
    path('userapp/workerprofile/<int:pk>/', login_required(ProfileView.as_view()),
         name="workerprofile"),
    # list of applied jobs
    path('userapp/workerprofile/appliedjobs', login_required(JobsAppliedListView.as_view()),
         name="appliedjobs"),
    # list of completeed jobs
    path('userapp/workerprofile/completedjobs', login_required(JobsCompletedListView.as_view()),
         name="completedjobs"),

    # list of jobs in progress
    path('userapp/workerprofile/jobsonprogress', login_required(JobsInProgressListView.as_view()),
         name="josinprogress"),
    # update worker profile details
    path('userapp/updateworkerprofile/<int:pk>/', login_required(WorkerProfileUpdateView.as_view()),
         name="updateworkerprofile"),

    # client profile
    # profile details
    path('userapp/clientprofile/<int:pk>/', login_required(ClientProfileView.as_view()),
         name="clientprofile"),
    # list of posted jobs
    path('userapp/clientprofile/postedjobs/', login_required(ClientPostedJobView.as_view()),
         name="clientprofilepostedjobs"),
    # list of Jobs in progress
    path('userapp/clientprofile/inprogressjobs/', login_required(ClientInProgressJobView.as_view()),
         name="clientinprogressjobs"),
    # list of completed jobs
    path('userapp/clientprofile/completedjobs/', login_required(ClientCompletedJobs.as_view()),
         name="clientcompletedjobs"),
    # Changing status of the job
    path('userapp/job/<int:pk>/update_status/', JobStatusUpdateView.as_view(),
         name='job_update_status'),
    # List of proposals for a job
    path('userapp/job/proposals/<int:job_id>/', JobProposalsView.as_view(),
         name='job_proposals'),
    # Detail of a proposal
    path('userapp/job/proposal_detail/<int:pk>/', ProposalDetailView.as_view(),
         name='proposal_detail'),
    # Proposal acception
    path('userapp/job/proposal_detail/acceptproposal<int:pk>', AcceptProposalView.as_view(),
         name='accept_proposal'),

    # rating and review
    path('userapp/clientprofile/rate&review/<int:job_id>/', ReviewModalView.as_view(), name="rateandreview"),
    path('userapp/clientprofile/submitreview/<int:job_id>/', SubmitReviewView.as_view(), name="submitreview"),


]
