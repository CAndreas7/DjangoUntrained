from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse
from Management.models import Course, Section, User
from Management.views import sections, sectionAdd, sectionEdit, sectionDelete, courses



class SectionsViewTest(TestCase):
    def setUp(self):
        self.taOld = User(email="taOld@uwm.edu", password="taOldpassword", phone="", role=3)
        self.taNew = User(email="taNew@uwm.edu", password="taNewpassword", phone="", role=3)
        self.courseMUS001 = Course(1, "MUS001", "Just like a wartime novelty.", "MUS")
        self.courseCS911 = Course(911, "CS911", "Emergency computer science, enroll immediately.", "CS")
        self.section001 = Section(sectionID=1, location="Backyard", startTime="12:00PM", endTime="12:01PM", capacity=30, TA=self.taOld, courseID=self.courseMUS001)


    def test_getID(self):
        tempSectionID = self.section001.getID()
        self.assertEqual(tempSectionID, self.section001.sectionID, msg="getSectionID did not return the correct sectionID")
        # response = self.client.get(reverse('sections', args=[self.course.courseID]))
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'main/sections.html')
        # self.assertContains(response, 'Test Course')
        # self.assertContains(response, '1')

    def test_getLocation(self):
        tempLocation = self.section001.getLocation()
        self.assertEqual(tempLocation, self.section001.location, msg="getSectionLocation did not return the correct location")

    def test_setLocation(self):
        self.section001.setLocation("MUS150")
        self.assertEqual("MUS150", self.section001.location, msg="setSectionLocation did not work correctly")
    def test_getStart(self):
        tempStart = self.section001.getStart()
        self.assertEqual(tempStart, self.section001.startTime, msg="getSectionStart did not return the correct start time")

    def test_setStart(self):
        self.section001.setStart("12:00AM")
        self.assertEqual("12:00AM", self.section001.startTime, msg="setSectionStart did not work correctly")

    def test_getEnd(self):
        tempEnd = self.section001.getEnd()
        self.assertEqual(tempEnd, self.section001.endTime, msg="getSectionEnd did not return the correct end time")

    def test_setEnd(self):
        self.section001.setEnd("12:01AM")
        self.assertEqual("12:01AM", self.section001.endTime, msg="setSectionEnd did not work correctly")

    def test_getCapacity(self):
        capacity = self.section001.getCapacity()
        self.assertEqual(capacity, self.section001.capacity, msg="getCapacity did not return the correct capacity")

    def test_setCapacity(self):
        self.section001.setCapacity(1)
        self.assertEqual(1, self.section001.capacity, msg="setCapacity did not work correctly")

    def test_getTA(self):
        TA = self.section001.getTA()
        self.assertEqual(TA, self.section001.TA, msg="getTA did not return the correct TA")

    def test_setTA(self):
        self.section001.setTA(self.taNew)
        self.assertEqual(self.taNew, self.section001.TA, msg="setTA did not work correctly")

    def test_getCourseID(self):
        courseID = self.section001.getCourseID()
        self.assertEqual(courseID, self.section001.courseID, msg="getCourseID did not return the correct course ID")

    def test_setCourseID(self):
        self.section001.setCourseID(self.courseCS911)
        self.assertEqual(self.courseCS911, self.section001.courseID, msg="setCourseID did not work correctly")

    # def test_delete(self):

#
# class SectionAddViewTest(TestCase):
#     def setUp(self):
#         self.course = Course.objects.create(courseID=1, courseName='Test Course')
#
#     def test_get(self):
#         response = self.client.get(reverse('sectionAdd', args=[self.course.courseID]))
#         # self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'main/addSection.html')
#
#     def test_post(self):
#         # Create a dictionary with the data to be submitted in the POST request
#         post_data = {
#             'courseID': self.course.courseID,
#             'sectionID': 1,
#             'location': 'Test Location',
#             'startTime': '09:00',
#             'endTime': '10:00',
#             'capacity': 30
#         }
#
#         # Send a POST request to the sectionAdd URL with the post_data
#         response = self.client.post(reverse('sectionAdd', args=[self.course.courseID]), post_data)
#
#         # Check that a new Section object was created in the database
#         self.assertTrue(Section.objects.filter(sectionID=1).exists())
#
#         # Get the newly created Section object from the database
#         section = Section.objects.get(sectionID=1)
#
#         # Check that the attributes of the new Section object match the data submitted in the POST request
#         self.assertEqual(section.location, post_data['location'])
#         self.assertEqual(section.startTime, post_data['startTime'])
#         self.assertEqual(section.endTime, post_data['endTime'])
#         self.assertEqual(section.capacity, post_data['capacity'])
#
#
# class TestSectionEditView(TestCase):
#     pass
#
#
# class SectionDeleteViewTest(TestCase):
#     def setUp(self):
#         self.course = Course.objects.create(courseID=1, courseName='Test Course')
#         self.section = Section.objects.create(courseID=self.course, sectionID=1, capacity=30)
#
#     def test_get(self):
#         response = self.client.get(reverse('sectionDelete', args=[self.course.courseID, self.section.sectionID]))
#         self.assertEqual(response.status_code, 302)
#         with self.assertRaises(Section.DoesNotExist):
#             Section.objects.get(pk=self.section.sectionID)
#
#
# class CoursesViewTest(TestCase):
#     def setUp(self):
#         self.course = Course.objects.create(courseID=1, courseName='Test Course')
#         self.section = Section.objects.create(courseID=self.course, sectionID=1, capacity=30)
#
#     def test_get(self):
#         response = self.client.get(reverse('courses'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "main/courses.html")
