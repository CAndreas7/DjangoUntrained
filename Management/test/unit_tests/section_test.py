from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse
from Management.models import Course, Section
from Management.views import sections, sectionAdd, sectionEdit, sectionDelete, courses
from django.contrib.auth.models import User


class SectionsViewTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(courseID=1, courseName='Test Course')
        self.section = Section.objects.create(courseID=self.course, sectionID=1, capacity=30)

    def test_get(self):
        response = self.client.get(reverse('sections', args=[self.course.courseID]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/sections.html')
        self.assertContains(response, 'Test Course')
        self.assertContains(response, '1')


class SectionAddViewTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(courseID=1, courseName='Test Course')

    def test_get(self):
        response = self.client.get(reverse('sectionAdd', args=[self.course.courseID]))
        # self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/addSection.html')

    def test_post(self):
        # Create a dictionary with the data to be submitted in the POST request
        post_data = {
            'courseID': self.course.courseID,
            'sectionID': 1,
            'location': 'Test Location',
            'startTime': '09:00',
            'endTime': '10:00',
            'capacity': 30
        }

        # Send a POST request to the sectionAdd URL with the post_data
        response = self.client.post(reverse('sectionAdd', args=[self.course.courseID]), post_data)

        # Check that a new Section object was created in the database
        self.assertTrue(Section.objects.filter(sectionID=1).exists())

        # Get the newly created Section object from the database
        section = Section.objects.get(sectionID=1)

        # Check that the attributes of the new Section object match the data submitted in the POST request
        self.assertEqual(section.location, post_data['location'])
        self.assertEqual(section.startTime, post_data['startTime'])
        self.assertEqual(section.endTime, post_data['endTime'])
        self.assertEqual(section.capacity, post_data['capacity'])


class TestSectionEditView(TestCase):
    pass


class SectionDeleteViewTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(courseID=1, courseName='Test Course')
        self.section = Section.objects.create(courseID=self.course, sectionID=1, capacity=30)

    def test_get(self):
        response = self.client.get(reverse('sectionDelete', args=[self.course.courseID, self.section.sectionID]))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Section.DoesNotExist):
            Section.objects.get(pk=self.section.sectionID)


class CoursesViewTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(courseID=1, courseName='Test Course')
        self.section = Section.objects.create(courseID=self.course, sectionID=1, capacity=30)

    def test_get(self):
        response = self.client.get(reverse('courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/courses.html")
