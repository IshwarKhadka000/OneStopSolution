from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import related


# models
class Service(models.Model):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True,blank=True)
    updated_on = models.DateField(auto_now = True, blank=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.name


gender_choices = (
    ('male', 'male'),
    ('female', 'female'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    experience = models.PositiveIntegerField(blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    skill = models.ManyToManyField(Skill)
    gender = models.CharField(choices=gender_choices, max_length=20, default='male')
    image = models.ImageField(upload_to='Profile/Images', blank=True, null=True)
    document = models.FileField(upload_to='Profile/Documents', blank=True, null=True)
    status = models.BooleanField(null=True, blank=True)
    fee = models.PositiveIntegerField(default=False, null=True, blank=True)
    active = models.BooleanField(null=True, blank=True)
    joined_on = models.DateField(auto_now_add=True, null=True)
    updated_on = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return self.user.username


class Job(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    postedby = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True, null=True)
    timetocomplete = models.PositiveIntegerField(blank=True, null=True)
    experience = models.PositiveIntegerField(blank=True, null=True)
    payment = models.PositiveIntegerField(blank=True, null=True)
    deadline = models.DateField(null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    skill = models.ManyToManyField(Skill)
    image = models.ImageField(upload_to='Job/Images', blank=True, null=True)
    requirements = models.TextField(max_length=2000, blank=True, null=True)
    description = models.TextField(max_length=2000, blank=True, null=True)
    posted_on = models.DateField(auto_now_add=True, null=True)
    modified_on = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return self.title

    def requirements_list(self):
        return self.requirements.split(',')

    # @property
    # def get_profile_count(self):
    #     return self.applied_by.all().count()
    # @property
    # def get_appliied_by(self):
    #     return self.applied_by.all()


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=150)
    message = models.TextField(max_length=500)
    sent_on = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.subject


class Proposal(models.Model):
    applied_to = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='proposed_job')
    amount = models.PositiveIntegerField(null=True, blank=True)
    applied_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="applied_profile")
    applied_on = models.DateField(auto_now_add=True)
    cover_letter = models.TextField(blank=True, null=True)
