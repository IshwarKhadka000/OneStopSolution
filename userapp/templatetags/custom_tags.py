from django import template

from userapp.models import Profile

register = template.Library()


def has_user_profile(value):
    has_profile = False
    profile_users = Profile.objects.values_list('user', flat=True)
    if value.id in profile_users:
        has_profile = True
    return has_profile


register.filter('has_user_profile', has_user_profile)
