from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from userapp.forms import *


# Create your views here.

class IndexView(TemplateView):
    template_name = 'pages/index.html'


class ContactView(TemplateView):
    template_name = 'pages/contact.html'


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class JobListView(TemplateView):
    template_name = 'pages/job-list.html'


class JobCategoryView(TemplateView):
    template_name = 'pages/jobcategory.html'


class JobDetailView(TemplateView):
    template_name = 'pages/job-detail.html'


class TestimonialView(TemplateView):
    template_name = 'pages/testimonial.html'


class ErrorPageView(TemplateView):
    template_name = 'pages/404.html'


class TalentListView(TemplateView):
    template_name = 'pages/talent-list.html'


class LoginView(FormView):
    print('Heree is the error')
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
