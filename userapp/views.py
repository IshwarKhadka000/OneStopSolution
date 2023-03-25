from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Q
from django.db.models.fields import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from userapp.forms import *


# Create your views here.


class IndexView(TemplateView):
    template_name = 'user/pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = Service.objects.all()
        service_job_count = []
        for service in services:
            job_count = Job.objects.filter(service=service, status='active').count()
            service_job_count.append((service, job_count))
        context['service_job_count'] = service_job_count
        context['jobs'] = Job.objects.filter(status='active')
        context['services'] = services
        return context


class AboutView(TemplateView):
    template_name = 'user/pages/about.html'


# workerprofile
class ProfileView(DetailView):
    model = User
    template_name = 'user/pages/workerprofile/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['skills'] = Skill.objects.all()
        return context


class JobsAppliedListView(TemplateView):
    template_name = 'user/pages/workerprofile/jobsapplied.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = self.request.user.profile
        context['proposals'] = Proposal.objects.filter(applied_by=profile_id)
        return context


class JobsCompletedListView(TemplateView):
    model = Job
    template_name = 'user/pages/workerprofile/jobscompleted.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = self.request.user.profile
        context['jobscompleted'] = Job.objects.filter(assigned_to=profile_id, status='completed')

        return context


class JobsInProgressListView(TemplateView):
    model = Job
    template_name = 'user/pages/workerprofile/jobsinprogress.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = self.request.user.profile
        context['jobsinprogress'] = Job.objects.filter(assigned_to=profile_id, status='inprogress')
        return context


class WorkerNotificationView(TemplateView):
    template_name = 'user/pages/workerprofile/notifications.html'


class JobListView(ListView):
    model = Job
    queryset = Job.objects.filter(status='active')
    template_name = 'user/pages/job-list.html'
    context_object_name = 'jobs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['skills'] = Skill.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(~Q(postedby=self.request.user.id))
        return queryset


class FilterJobListView(View):
    template_name = 'user/pages/filtered_joblist.html'

    def get_experience_queryset(self, value):
        queryset = Job.objects.all()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(~Q(postedby=self.request.user.id))
        if value == 1:
            queryset = set(queryset.filter(experience__lte=1).values_list('id', flat=True))
        if value == 2:
            queryset = set(queryset.filter(experience__lte=3, experience__gte=1).values_list('id', flat=True))
        if value == 3:
            queryset = set(queryset.filter(experience__lte=5, experience__gte=3).values_list('id', flat=True))
        if value == 4:
            queryset = set(queryset.filter(experience__gte=5).values_list('id', flat=True))
        return queryset

    def get_queryset(self):
        queryset = Job.objects.filter(status='active')
        if self.request.user.is_authenticated:
            queryset = queryset.filter(~Q(postedby=self.request.user.id))
        if self.request.GET:
            minimum_fee = self.request.GET.get('minimum_fee')
            maximum_fee = self.request.GET.get('maximum_fee')
            service = list(map(int, self.request.GET.getlist('service[]')))
            experience = list(map(int, self.request.GET.getlist('experience[]')))
            skill = list(map(int, self.request.GET.getlist('skill[]')))
            if experience:
                main_set = set()
                set_1 = set()
                set_2 = set()
                set_3 = set()
                set_4 = set()
                if 1 in experience:
                    set_1 = self.get_experience_queryset(1)
                if 2 in experience:
                    set_2 = self.get_experience_queryset(2)
                if 3 in experience:
                    set_3 = self.get_experience_queryset(3)
                if 4 in experience:
                    set_4 = self.get_experience_queryset(4)
                main_set = main_set.union(set_1, set_2, set_3, set_4)

                queryset = queryset.filter(id__in=main_set)

            queryset = queryset.filter(payment__gte=minimum_fee, payment__lte=maximum_fee).distinct()
            if service:
                queryset = queryset.filter(service__in=service).distinct()

            if skill:
                queryset = queryset.filter(skill__in=skill).distinct()
        return queryset

    def get(self, request, *args, **kwargs):
        context = dict()
        context['jobs'] = self.get_queryset()
        context['services'] = Service.objects.all()
        context['skills'] = Skill.objects.all()
        return render(request, self.template_name, context)


class TalentListView(ListView):
    model = Profile
    template_name = 'user/pages/talent-list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(~Q(user=self.request.user.id))

        queryset = sorted(queryset, key=lambda x: x.get_avg_rating, reverse=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['skills'] = Skill.objects.all()

        return context


class FilterTalentListView(View):
    template_name = 'user/pages/filtered_talentlist.html'

    def get_experience_queryset(self, value):
        queryset = Profile.objects.all()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(~Q(user=self.request.user.id))

        if value == 1:
            queryset = set(queryset.filter(experience__lte=1).values_list('id', flat=True))
        if value == 2:
            queryset = set(queryset.filter(experience__lte=3, experience__gte=1).values_list('id', flat=True))
        if value == 3:
            queryset = set(queryset.filter(experience__lte=5, experience__gte=3).values_list('id', flat=True))
        if value == 4:
            queryset = set(queryset.filter(experience__gte=5).values_list('id', flat=True))
        return queryset

    def get_queryset(self):
        queryset = Profile.objects.all()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(~Q(user=self.request.user.id))

        if self.request.GET:
            minimum_fee = self.request.GET.get('minimum_fee')
            maximum_fee = self.request.GET.get('maximum_fee')
            service = list(map(int, self.request.GET.getlist('service[]')))
            experience = list(map(int, self.request.GET.getlist('experience[]')))
            skill = list(map(int, self.request.GET.getlist('skill[]')))

            if experience:
                main_set = set()
                set_1 = set()
                set_2 = set()
                set_3 = set()
                set_4 = set()
                if 1 in experience:
                    set_1 = self.get_experience_queryset(1)
                if 2 in experience:
                    set_2 = self.get_experience_queryset(2)
                if 3 in experience:
                    set_3 = self.get_experience_queryset(3)
                if 4 in experience:
                    set_4 = self.get_experience_queryset(4)
                main_set = main_set.union(set_1, set_2, set_3, set_4)

                queryset = queryset.filter(id__in=main_set)

            queryset = queryset.filter(fee__gte=minimum_fee, fee__lte=maximum_fee).distinct()
            if service:
                queryset = queryset.filter(service__in=service).distinct()

            if skill:
                queryset = queryset.filter(skill__in=skill).distinct()
            queryset = sorted(queryset, key=lambda x: x.get_avg_rating, reverse=True)

        return queryset

    def get(self, request, *args, **kwargs):
        context = dict()
        context['profiles'] = self.get_queryset()
        context['services'] = Service.objects.all()
        context['skills'] = Skill.objects.all()
        return render(request, self.template_name, context)


class TalentDetailView(DetailView):
    model = User
    template_name = 'user/pages/talent-detail.html'
    context_object_name = 'worker'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_object = Profile.objects.get(user=self.kwargs['pk'])
        profile_id = profile_object.id
        context['reviews'] = Review.objects.filter(profile=profile_id)

        rating_counts = (
            Review.objects
            .filter(profile_id=profile_id)
            .values('rating')
            .annotate(count=models.Count('rating'))
            .order_by('-rating')
        )

        count_dict = {str(i): 0 for i in range(1, 6)}
        total_count = 0
        total_rating = 0
        for rating_count in rating_counts:
            count_dict[str(rating_count['rating'])] = rating_count['count']
            total_count += rating_count['count']
            total_rating += rating_count['count'] * rating_count['rating']

        if total_count > 0:
            average_rating = total_rating / total_count
            context['average_rating'] = round(average_rating, 2)
            context['rating_counts'] = count_dict
            context['total_count'] = total_count
            complete_stars = int(average_rating)
            context['complete_stars'] = str(complete_stars)
            percent_filled = round((average_rating % 1) * 100, 2)
            context['percent_filled'] = percent_filled
            if percent_filled > 0:
                context['remaining_stars'] = str(5 - complete_stars - 1)
            else:
                context['remaining_stars'] = str(5 - complete_stars)

        return context


class JobCategoryView(TemplateView):
    template_name = 'user/pages/jobcategory.html'


def has_related_object(user):
    try:
        user.profile
        return True
    except ObjectDoesNotExist:
        return False


class CategoryJobListView(ListView):
    model = Job
    template_name = 'user/pages/categoryjob.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        service = self.kwargs['service']
        return Job.objects.filter(service=service, status='active')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = Service.objects.get(pk=self.kwargs['service'])
        context['service'] = service
        return context


class JobDetailView(DetailView):
    model = Job
    template_name = 'user/pages/job-detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.object.id
        now = datetime.now()
        context['time_remaining'] = (datetime.combine(
            self.object.deadline, datetime.min.time()) - now).days

        if has_related_object(self.request.user):
            user = self.request.user.profile
            context['has_applied'] = Proposal.objects.filter(applied_to=job_id, applied_by=user).exists()
            context['proposals'] = Proposal.objects.filter(applied_to=job_id).count()
        else:
            context['no_profile'] = True

        return context


class MarkJobCompleted(UpdateView):
    model = Job
    fields = ('status',)
    success_url = reverse_lazy('settings')
    success_message = 'Job marked as completed successfully'


# class EditJobView(UpdateView):
#     model = Job
#     form_class = JobCreateForm
#     context_object_name = 'job'
#     template_name = 'user/pages/job_edit_modal.html'
#     success_url = reverse_lazy('clientprofile')


class JobProposalCreateView(CreateView):
    model = Proposal
    form_class = SendProposalForm

    def get_job(self):
        job_obj = get_object_or_404(Job, pk=self.kwargs.get('jobid'))
        return job_obj

    def form_valid(self, form):
        job_id = self.get_job()
        form.instance.applied_by = self.request.user.profile
        form.instance.applied_to = job_id
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, "Proposal sent successfully")
        return reverse_lazy('jobdetail', kwargs={'pk': self.kwargs.get('jobid')})


class TestimonialView(TemplateView):
    template_name = 'user/pages/testimonial.html'


class ErrorPageView(TemplateView):
    template_name = 'user/pages/404.html'


class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('index')
    template_name = 'user/pages/login.html'

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            # A backend authenticated the credentials
            login(self.request, user)
            messages.success(self.request, "logged in successfully")
            return redirect('index')
        else:
            messages.warning(self.request, "User is not authenticated")
            return redirect('login')


class LogoutView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        logout(request)
        messages.success(request, "User logged out successfully")
        return redirect('index')


class RegistrationView(SuccessMessageMixin, CreateView):
    form_class = NewUserForm
    template_name = 'user/pages/registration.html'
    success_url = reverse_lazy('login')
    success_message = 'User account registered successfully'


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('login')
    template_name = 'user/pages/changepassword.html'
    success_message = "Password Changed successfully!! Please login again using new password"


class BecomeWorkerView(FormView):
    form_class = WorkerProfileForm
    success_url = reverse_lazy('index')
    template_name = 'user/pages/becomeworker.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['skills'] = Skill.objects.all()
        return context

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()
        skills = form.cleaned_data['skill']
        profile.skill.add(*skills)
        messages.success(self.request, 'Registration details submitted successfully')
        return redirect('index')


class WorkerProfileUpdateView(UpdateView):
    form_class = WorkerProfileForm
    queryset = Profile.objects.all()
    template_name = 'user/pages/workerprofile/profile.html'
    success_url = reverse_lazy('workerprofile')

    def form_valid(self, form):
        email = self.request.POST.get('email')
        profile = form.save(commit=False)
        profile.save()
        skills = form.cleaned_data.get('skill')
        if skills:
            pass
            s = profile.skill.all()
            if s:
                profile.skill.remove(*s)
            profile.skill.add(
                *skills
            )
            # profile.skill.set(*skills, clear=True)

        user = profile.user
        user.email = email
        user.save()
        messages.success(self.request, 'Profile details updated successfully')
        return redirect('workerprofile', pk=profile.user.pk)

    def form_invalid(self, form):
        profile = self.get_object()
        user = profile.user
        return redirect('workerprofile', pk=profile.user.pk)


class JobPostView(CreateView):
    form_class = JobCreateForm
    success_url = reverse_lazy('index')
    template_name = 'user/pages/postajob.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['skills'] = Skill.objects.all()
        return context

    def form_valid(self, form):
        job = form.save(commit=False)
        job.postedby = self.request.user
        job.save()
        skills = form.cleaned_data['skill']
        job.skill.add(*skills)
        messages.success(self.request, 'New job created successfully')

        return redirect('index')

    def form_invalid(self, form):
        for field in form.errors:
            messages.error(self.request, f"{field}: {form.errors[field][0]}")
        return super().form_invalid(form)


class ContactView(SuccessMessageMixin, CreateView):
    form_class = ContactForm
    template_name = 'user/pages/contact.html'

    success_message = 'Query submitted successfully !! We will get back to you as soon as possible'
    success_url = reverse_lazy('index')



class SendProposalView(CreateView):
    model = Proposal
    form_class = SendProposalForm


# client profile
class ClientProfileView(DetailView):
    model = User
    template_name = 'user/pages/clientprofile/profile.html'
    context_object_name = 'user'


class ClientPostedJobView(TemplateView):
    template_name = 'user/pages/clientprofile/jobsposted.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posted_jobs'] = Job.objects.filter(postedby=self.request.user, status='active')
        return context


class ClientInProgressJobView(TemplateView):
    template_name = 'user/pages/clientprofile/jobsinprogress.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inprogress_jobs'] = Job.objects.filter(postedby=self.request.user, status='inprogress')
        context['inprogress_jobs_count'] = context['inprogress_jobs'].count()
        return context


class ClientCompletedJobs(TemplateView):
    template_name = 'user/pages/clientprofile/jobscompleted.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completed_jobs'] = Job.objects.filter(postedby=self.request.user, status='completed')
        return context


class JobProposalsView(TemplateView):
    template_name = 'user/pages/clientprofile/jobproposals.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.kwargs.get('job_id')
        context['job'] = Job.objects.get(id=job_id)
        context['proposals'] = Proposal.objects.filter(applied_to=job_id)
        return context


class JobStatusUpdateView(UpdateView):
    model = Job
    fields = ['status']

    def get(self, request, *args, **kwargs):
        job = self.get_object()
        job.status = 'completed'
        job.save()
        messages.success(request, "Job marked as completed successfully")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('rateandreview', kwargs={'job_id': self.get_object().pk})


class ReviewModalView(TemplateView):
    template_name = 'user/pages/clientprofile/profile_rating_modal.html'
    form_class = ProvideReviewForm
    model = Review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.kwargs.get('job_id')
        job = Job.objects.get(id=job_id)
        context['job'] = job
        return context


class SubmitReviewView(View):

    def get(self, request, *args, **kwargs):
        redirect_url = reverse('clientinprogressjobs')
        userrating = request.GET.get('userrating')
        review_by = request.GET.get('review_by')
        review = request.GET.get('review')
        job_id = request.GET.get('job_id')
        profile = request.GET.get('profile')
        hasreview = Review.objects.filter(job=job_id).exists()
        if not hasreview:
            review_obj = Review()
            review_obj.rating = userrating
            review_obj.profile = Profile.objects.get(id=profile)
            review_obj.job = Job.objects.get(id=job_id)
            review_obj.review = review
            review_obj.review_by = User.objects.get(id=review_by)
            review_obj.save()
            messages.success(request, 'Your review has been submitted!')
            return JsonResponse({'status': 'success', 'redirect_url': redirect_url})
        else:
            messages.warning(request, 'Review already submitted!')
            return JsonResponse({'status': 'success', 'redirect_url': redirect_url})


class ClientNotificationView(TemplateView):
    template_name = 'user/pages/clientprofile/notifications.html'


class NewsLetterSubscribeView(FormView):
    template_name = 'user/layouts/footer.html'


class ProposalDetailView(DetailView):
    model = Proposal
    context_object_name = 'proposal'
    template_name = 'user/pages/clientprofile/proposaldetail.html'


class AcceptProposalView(View):

    def post(self, request, *args, **kwargs):
        proposal = get_object_or_404(Proposal, id=self.kwargs['pk'])
        print(proposal)
        job = proposal.applied_to
        job.status = 'inprogress'
        job.assigned_to = proposal.applied_by
        job.save()
        messages.success(request, "Proposal accepted successfully")
        return redirect(reverse('clientprofile', args=[request.user.id]))
