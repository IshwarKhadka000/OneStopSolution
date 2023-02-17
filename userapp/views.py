from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from userapp.forms import *


# Create your views here.

class IndexView(TemplateView):
    template_name = 'pages/index.html'


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class ProfileView(TemplateView):
    template_name = 'pages/profile.html'


class JobListView(ListView):
    model = Job
    template_name = 'pages/job-list.html'
    context_object_name = 'jobs'


class TalentListView(ListView):
    model = Profile
    template_name = 'pages/talent-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_ids = Profile.objects.values_list('user', flat=True)
        context['users'] = User.objects.filter(id__in=profile_ids)
        return context


class TalentDetailView(DetailView):
    model = User
    template_name = 'pages/talent-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_object()
        return context


class JobCategoryView(TemplateView):
    template_name = 'pages/jobcategory.html'


class JobDetailView(DetailView):
    model = Job
    template_name = 'pages/job-detail.html'
    context_object_name = 'job'


class TestimonialView(TemplateView):
    template_name = 'pages/testimonial.html'


class ErrorPageView(TemplateView):
    template_name = 'pages/404.html'


class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('index')
    template_name = 'pages/login.html'

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
    template_name = 'pages/registration.html'
    success_url = reverse_lazy('login')
    success_message = 'User account registered successfully'


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('login')
    template_name = 'pages/changepassword.html'
    success_message = "Password Changed successfully!! Please login again using new password"


class BecomeWorkerView(FormView):
    form_class = WorkerProfileForm
    success_url = reverse_lazy('index')
    template_name = 'pages/becomeworker.html'

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


class JobPostView(FormView):
    form_class = JobCreateForm
    success_url = reverse_lazy('index')
    template_name = 'pages/postajob.html'

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
        print('Hereee')
        messages.success(self.request, 'New job created successfully')
        return redirect('index')


class ContactView(SuccessMessageMixin, CreateView):
    form_class = ContactForm
    template_name = 'pages/contact.html'
    success_url = reverse_lazy('index')
    success_message = 'Query submitted successfully !! We will get back to you as soon as possible'
