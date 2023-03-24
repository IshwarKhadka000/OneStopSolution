from django import forms
from django.contrib.auth.forms import AuthenticationForm

from userapp.models import *


class AdminLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password',)


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('name',)


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name',)


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ('name',)


class WorkerStatusForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('status',)
