import unittest
from Management.models import Course, Section, User
from django.test import TestCase

class TestCourse(TestCase):

    def setUp(self):
        self.courseCS250 = Course(1, "CS250", "Some elementary comp sci class", "CS")
        self.courseCS350 = Course(2, "CS350", "Some mediumentary comp sci class", "CS")
        self.courseNotCS = Course(3, "Chemistry 100", "Yuck, some natural science class", "Chemistry")
    def test_getName(self):
        name = self.courseCS250.getName()
        self.assertEqual(name, self.courseCS250.name, msg="Returned name was not the course's name")
    def test_setName(self):
        self.courseCS250.setName("NotCS250")
        self.assertEqual("NotCS250", self.courseCS250.name, msg="Tried to set the name of the course but "
                                                                     "didn't corrently store the new course name.")
    def test_getDescription(self):
        description = self.courseCS250.getDescription()
        self.assertEqual("Some elementary comp sci class", self.courseCS250.courseDescription,
                         msg="returned course description was not the course's description")
    def test_setDescription(self):
        self.courseCS250.setDescription("I love green eggs.")
        self.assertEqual("I love green eggs.", self.courseCS250.courseDescription, msg="course description"
                                                                                       "wasn't set properly.")
    def test_getDepartment(self):
        department = self.courseCS250.getDepartment()
        self.assertEqual("CS", self.courseCS250.courseDepartment,
                         msg="returned department is not the course's department.")
    def test_setDepartment(self):
        department = self.courseCS250.setDepartment("yolo")
        self.assertEqual("yolo", self.courseCS250.courseDepartment,
                         msg="department wasn't set properly.")
    def test_addSection(self):
        """ mockSection = Section(1, "England", "1PM", "10PM", 300, User("taemail@uwm.edu", "mypass", "", 3), 2)"""

        mockSection = "mock"
        self.courseCS350.addSection(mockSection)
        self.assertEqual(mockSection, courseCS350.Section[0], msg="Added section is not added to the section array"
                                                                  "in courses")

    def test_removeSection(self):
        """mockSection = Section(1, "England", "1PM", "10PM", 300, User("taemail@uwm.edu", "mypass", "", 3), 2)"""
        mockSection = "mock"
        self.courseCS350.addSection(mockSection)
        self.courseCS350.removeSection(mockSection.getID())
        self.assertEqual(None, courseCS350.Section[0], msg="Added section is not removed from the section array in "
                                                           "courses")

