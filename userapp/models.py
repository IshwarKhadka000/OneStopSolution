from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Avg
from django.db.models.fields import related


# models
class Service(models.Model):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True, blank=True)
    updated_on = models.DateField(auto_now=True, blank=True)

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


class Status(models.Model):
    name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=2500, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    experience = models.PositiveIntegerField(blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    skill = models.ManyToManyField(Skill)
    gender = models.CharField(choices=gender_choices, max_length=20, default='male')
    image = models.ImageField(upload_to='Profile/Images', blank=True, null=True)
    document = models.FileField(upload_to='Profile/Documents', blank=True, null=True)
    fee = models.PositiveIntegerField(default=False, null=True, blank=True)
    active = models.BooleanField(null=True, blank=True)
    joined_on = models.DateField(auto_now_add=True, null=True)
    updated_on = models.DateField(auto_now=True, null=True)
    status = models.ForeignKey(Status, blank=True, null=True, default="", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @property
    def get_avg_rating(self):
        return self.profile_ratings.aggregate(Avg('rating')).get("rating__avg") \
            if self.profile_ratings.exists() else 0.0

    @property
    def get_number_of_ratings(self):
        return self.profile_ratings.count()

    @property
    def rating_breakdown(self):
        avg_rating = round(self.get_avg_rating, 2)
        complete_stars = int(avg_rating)
        percent_filled = round((avg_rating % 1) * 100, 2)
        if percent_filled > 0:
            remaining_stars = (5 - complete_stars - 1)
        else:
            remaining_stars = (5 - complete_stars)
        return {'complete_stars': str(complete_stars), 'percent_filled': percent_filled,
                'remaining_stars': str(remaining_stars)}


job_status = (
    ('active', 'active'),
    ('inprogress', 'inprogress'),
    ('not completed', 'not completed'),
    ('completed', 'completed'),
)


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
    status = models.CharField(choices=job_status, max_length=20, default="active")
    assigned_to = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)

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


proposal_status = (
    ('applied', 'applied'),
    ('accepted', 'accepted'),
    ('rejected', 'rejected'),
)


class Proposal(models.Model):
    applied_to = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='proposed_job')
    amount = models.PositiveIntegerField(null=True, blank=True)
    applied_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="applied_profile")
    applied_on = models.DateField(auto_now_add=True)
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(choices=proposal_status, max_length=20, default='applied')


class Review(models.Model):
    rating = models.PositiveBigIntegerField(null=True, blank=True)
    profile = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE,
                                related_name="profile_ratings")
    job = models.OneToOneField(Job, null=True, blank=True, on_delete=models.CASCADE, related_name="job_rating")
    review = models.TextField(max_length=200, null=True, blank=True)
    review_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="rated_by")
    reviewed_on = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.review_by.username

    @classmethod
    def get_avg_rating_per_profile(cls):
        return cls.objects.values('profile').annotate(avg_rating=Avg('rating'), num_ratings=Count('rating')).order_by(
            '-avg_rating')

