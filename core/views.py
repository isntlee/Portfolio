from django.shortcuts import render
from allauth.account.views import SignupView

from core.forms import VolunteerSignupForm

class VolunteerSignUpView(SignupView):
    template_name = 'account/volunteer_signup.html'
    form_class = VolunteerSignupForm
