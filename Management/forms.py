from django import forms
from .models import *


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['courseID', 'location', 'startTime', 'endTime', 'capacity', 'TA', 'sectionID']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['courseID', 'courseName', 'courseDescription', 'courseDepartment']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone']
class UserToFrom(forms.ModelForm):
    class Meta:
        model = UsersToCourse
        fields = ['assignment']

