from django.db import models

from django.contrib.auth.models import User


# models
class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


gender_choices = (
    ('male', 'male'),
    ('female', 'female'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    skill = models.ManyToManyField(Skill)
    gender = models.CharField(choices=gender_choices, max_length=20, default='male')
    image = models.ImageField(upload_to='Profile/Images', blank=True, null=True)
    document = models.FileField(upload_to='Profile/Documents', blank=True, null=True)
    status = models.BooleanField(null=True, blank=True)
    fee = models.PositiveIntegerField(null=True, blank=True)
    active = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.user.username

