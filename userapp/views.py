from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from userapp.forms import *
from captcha.fields import ReCaptchaField

# Create your views here.


class IndexView(TemplateView):
    template_name = 'user/pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = Service.objects.all()
        service_job_count = []
        for service in services:
            job_count = Job.objects.filter(service=service).count()
            service_job_count.append((service, job_count))
        context['service_job_count'] = service_job_count
        context['jobs'] = Job.objects.all()
        context['services'] = services
        return context


class AboutView(TemplateView):
    template_name = 'user/pages/about.html'


class SettingView(DetailView):
    model = User
    template_name = 'user/pages/settings.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = self.request.user.profile
        context['proposals'] = Proposal.objects.filter(applied_by=profile_id)
        context['services'] = Service.objects.all()
        context['skills'] = Skill.objects.all()
        return context


class JobListView(ListView):
    model = Job
    template_name = 'user/pages/job-list.html'
    context_object_name = 'jobs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['skills'] = Skill.objects.all()
        return context


class FilterJobListView(View):
    template_name = 'user/pages/filtered_joblist.html'

    def get_experience_queryset(self, value):
        queryset = Profile.objects.all()
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
        queryset = Job.objects.all()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['skills'] = Skill.objects.all()
        return context


class FilterTalentListView(View):
    template_name = 'user/pages/filtered_talentlist.html'

    def get_experience_queryset(self, value):
        queryset = Profile.objects.all()
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
    context_object_name = 'user'


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
        return Job.objects.filter(service=service)
    
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
        if has_related_object(self.request.user):
            user = self.request.user.profile
            context['has_applied'] = Proposal.objects.filter(applied_to=job_id, applied_by=user).exists()
            context['proposals'] = Proposal.objects.filter(applied_to=job_id).count()
        else:
            context['no_profile'] = True

        return context


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
    template_name = 'user/pages/settings.html'
    success_url = reverse_lazy('settings')

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
        return redirect('settings', pk=profile.user.pk)

    def form_invalid(self, form):
        profile = self.get_object()
        user = profile.user
        return redirect('settings', pk=profile.user.pk)


class JobPostView(FormView):
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


class ContactView(SuccessMessageMixin, CreateView):
    form_class = ContactForm
    template_name = 'user/pages/contact.html'
    success_url = reverse_lazy('index')
    success_message = 'Query submitted successfully !! We will get back to you as soon as possible'
    captcha = ReCaptchaField()

    def form_valid(self, form):
        if form.is_valid():
            captcha_response = self.request.POST.get('g-recaptcha-response')
            if self.captcha.verify(captcha_response):
                form.send_email()
                messages.success(self.request, 'Your message has been sent.')
                return super().form_valid(form)
            else:
                messages.error(
                    self.request, 'Invalid CAPTCHA, please try again.')
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)


class SendProposalView(CreateView):
    model = Proposal
    form_class = SendProposalForm


class ClientSettingView(DetailView):
    model = User
    template_name = 'user/pages/clientprofile.html'
    context_object_name = 'user'

class NewsLetterSubscribeView(FormView):
    template_name = 'user/layouts/footer.html'
    
