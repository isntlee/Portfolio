from django import forms
from allauth.account.forms import SignupForm 
from django.db import transaction
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from core.models import Volunteer, Skill

class VolunteerSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name') 
    last_name = forms.CharField(max_length=30, label='Last Name')

    # add all fields here which you have added in Volunteer model except user(OneToOneField)
    area = forms.CharField(max_length=100)
    select_country = CountryField(blank_label='(select country)').formfield(
        required = True,
        widget=CountrySelectWidget(attrs={
        }))
    skills = forms.ModelMultipleChoiceField(
            queryset=Skill.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=True
            )

    @transaction.atomic
    # Override the save method to save the extra fields
    # (otherwise the form will save the User instance only)
    def save(self, request):
         # Save the User instance and get a reference to it
        user = super(VolunteerSignupForm, self).save(request)
        # for volunteer account mark is_volunteer = True
        user.is_volunteer = True
        
        # Now Save extra fields in Volunteer model
        volunteer_user = Volunteer(
            user=user,
            area=self.cleaned_data.get('area'),
            select_country=self.cleaned_data.get('select_country'),
            # skills=self.cleaned_data.get('skills')
        )
        user.save()
        volunteer_user.save()

        volunteer_user.skills.add(*self.cleaned_data.get('skills'))

        # return user
        return user
