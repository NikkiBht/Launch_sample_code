from django import forms
from account.models import Account
from account.models import Profile
from django_countries.fields import CountryField


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user information.
    """

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name']


class ProfilePicUpdateForm(forms.ModelForm):
    """
    Form for updating profile picture.
    """

    class Meta:
        model = Profile
        fields = ['image']


class ProfileLocationForm(forms.ModelForm):
    """
    Form for updating profile location.
    """

    city = forms.CharField(max_length=100)
    contact = forms.CharField(max_length=300)

    class Meta:
        model = Profile
        fields = ['country', 'city', 'contact']


class AboutForm(forms.ModelForm):
    """
    Form for updating profile about information.
    """

    class Meta:
        model = Profile
        fields = ['about']


class ExperienceForm(forms.ModelForm):
    """
    Form for updating profile experience.
    """

    experience = forms.CharField(max_length=100)

    class Meta:
        model = Profile
        fields = ['experience']


class EducationForm(forms.ModelForm):
    """
    Form for updating profile education.
    """

    class Meta:
        model = Profile
        fields = ['education']


class SkillForm(forms.ModelForm):
    """
    Form for updating profile skills.
    """

    class Meta:
        model = Profile
        fields = ['skills']
