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
