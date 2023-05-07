from django import forms
from .models import *


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['location', 'startTime', 'endTime', 'capacity', 'TA', 'sectionID']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['courseID', 'courseName', 'courseDescription', 'courseDepartment']


class CourseEditForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['courseName', 'courseDescription', 'courseDepartment']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'lName', 'fName', 'password', 'phone', 'role']


class UserToFrom(forms.ModelForm):
    assignment = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = UsersToCourse
        fields = ['assignment']

    def clean_assignment(self):
        user = self.cleaned_data['assignment']
        return user.email
