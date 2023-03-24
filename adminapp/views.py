from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, View, UpdateView, CreateView, ListView, UpdateView, \
    DeleteView, FormView
from djlint import Config
from adminapp.forms import *
from userapp.models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
import time


# Create your views here.


class AdminLogin(View):
    template_name = 'admin/pages/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('dashboard')
        else:
            return redirect('adminlogin')

    @staticmethod
    def logout_view(request):
        logout(request)
        return redirect('adminlogin')


class AdminDashboardView(TemplateView):
    template_name = 'admin/pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(is_superuser=True).count()
        context['services'] = Service.objects.count()
        context['skills'] = Skill.objects.count()
        context['queries'] = Contact.objects.count()
        context['profiles'] = Profile.objects.count()
        context['jobs'] = Job.objects.count()
        return context


# services
class ServiceListView(ListView):
    model = Service
    ordering = "id"
    paginate_by = 3
    template_name = 'admin/pages/services.html'
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        current_page = int(self.request.GET.get('page', '1'))
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context


class AddServiceView(CreateView):
    model = Service
    ordering = "id"
    form_class = ServiceForm
    template_name = 'admin/pages/add_service_modal.html'
    success_url = reverse_lazy('service_list')


class EditServiceView(UpdateView):
    model = Service
    form_class = ServiceForm
    context_object_name = 'service'
    template_name = 'admin/pages/edit_service_modal.html'
    success_url = reverse_lazy('service_list')


class DeleteServiceView(View):
    def post(self, request, *args, **kwargs):
        service = get_object_or_404(Service, pk=self.kwargs.get('pk'))
        service.delete()
        return redirect('service_list')


# skill
class SkillListView(ListView):
    model = Skill
    ordering = "id"
    paginate_by = 1
    template_name = 'admin/pages/skills.html'
    context_object_name = 'skills'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        current_page = int(self.request.GET.get('page', '1'))
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context


class AddSkillView(CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'admin/pages/add_skill_modal.html'
    success_url = reverse_lazy('skill_list')


class EditSkillView(UpdateView):
    model = Skill
    form_class = SkillForm
    context_object_name = 'skill'
    template_name = 'admin/pages/edit_skill_modal.html'
    success_url = reverse_lazy('skill_list')


class DeleteSkillView(View):
    def post(self, request, *args, **kwargs):
        print('here')
        skill = get_object_or_404(Skill, pk=self.kwargs.get('pk'))
        skill.delete()
        return redirect('skill_list')


class ClientListView(ListView):
    model = User
    queryset = User.objects.all().exclude(is_superuser=True).order_by('id')
    ordering = "id"
    paginate_by = 1
    template_name = 'admin/pages/clients.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        current_page = int(self.request.GET.get('page', '1'))
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context


class WorkerListView(ListView):
    model = Profile
    ordering = "id"
    paginate_by = 1
    template_name = 'admin/pages/workers.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        current_page = int(self.request.GET.get('page', '1'))
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context


class EditWorkerStatusView(UpdateView):
    model = Profile
    form_class = WorkerStatusForm
    context_object_name = 'profile'
    template_name = 'admin/pages/edit_worker_status.html'
    success_url = reverse_lazy('worker_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        return context


class JobListView(ListView):
    model = Job
    ordering = "id"
    paginate_by = 1
    template_name = 'admin/pages/jobs.html'
    context_object_name = 'jobs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        current_page = int(self.request.GET.get('page', '1'))
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context


# Query
class QueryListView(ListView):
    model = Contact
    ordering = "id"
    paginate_by = 1
    template_name = 'admin/pages/queries.html'
    context_object_name = 'queries'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        current_page = int(self.request.GET.get('page', '1'))
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context


class QueryDetailView(DetailView):
    model = Contact

    template_name = 'admin/pages/query_detail_model.html'
    context_object_name = "query"


class DeleteQueryView(View):
    def post(self, request, *args, **kwargs):
        contact = get_object_or_404(Contact, pk=self.kwargs.get('pk'))
        contact.delete()
        return redirect('query_list')


# Status


class StatusListView(ListView):
    model = Status
    ordering = "id"
    paginate_by = 10
    template_name = 'admin/pages/status.html'
    context_object_name = 'statuses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        current_page = int(self.request.GET.get('page', '1'))
        start_index = int((current_page - 1) /
                          page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context


class AddStatusView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'admin/pages/add_status_modal.html'
    success_url = reverse_lazy('status_list')


class EditStatusView(UpdateView):
    model = Status
    form_class = StatusForm
    context_object_name = 'status'
    template_name = 'admin/pages/edit_status_modal.html'
    success_url = reverse_lazy('status_list')


class DeleteStatusView(View):
    def post(self, request, *args, **kwargs):
        status = get_object_or_404(Status, pk=self.kwargs.get('pk'))
        status.delete()
        return redirect('status_list')


class WorkerDetailView(DetailView):
    model = Profile
    template_name = 'admin/pages/worker_detail_model.html'
    context_object_name = "profile"


class JobDetailView(DetailView):
    model = Job
    template_name = 'admin/pages/job_detail_modal.html'
    context_object_name = "job"
