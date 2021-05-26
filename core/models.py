from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from django.conf import settings
from django_countries.fields import CountryField


class User(AbstractUser):
    is_volunteer = models.BooleanField(default=False)
    is_organisation = models.BooleanField(default=False)


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Volunteer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    select_country = CountryField(multiple=False)
    area = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill, related_name='interested_skills')

    def __str__(self):
        return self.user.username 



# https://stackoverflow.com/questions/44505242/multiple-user-type-sign-up-with-django-allauth