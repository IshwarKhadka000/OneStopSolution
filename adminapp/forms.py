from django import forms
from userapp.models import *


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
        model=Status
        fields = ('name',)

class WorkerStatusForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('status',)