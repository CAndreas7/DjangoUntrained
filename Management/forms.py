from django import forms
from .models import Course, Section


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['courseID', 'location', 'startTime', 'endTime', 'capacity', 'TA', 'sectionID']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['courseName', 'courseDescription', 'courseDepartment']
