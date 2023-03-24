from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import *


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput())


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class WorkerProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].widget.attrs.update({'class': 'form-control'})
        self.fields['skill'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Profile
        exclude = ['user']


class JobCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Job
        exclude = ['posted_on', 'modified_on', 'postedby', 'status']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']


class SendProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['applied_to', 'amount', 'applied_by', 'cover_letter']

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super().__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['applied_to'].required = False
        self.fields['applied_by'].required = False


class ProvideReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'profile', 'job', 'review', 'review_by', ]


