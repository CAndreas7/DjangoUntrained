import unittest

from django.core.exceptions import ValidationError

from Management.forms import CourseForm
from Management.models import Course, Section, User
from django.test import TestCase


class TestCourse(TestCase):

    def setUp(self):
        self.courseCS250 = Course(1, "CS250", "Some elementary comp sci class", "CS")
        self.courseCS350 = Course(2, "CS350", "Some mediumentary comp sci class", "CS")
        self.courseNotCS = Course(3, "Chemistry 100", "Yuck, some natural science class", "Chemistry")

    def test_getName(self):
        name = self.courseCS250.getName()
        self.assertEqual("CS250", name, msg="Returned name was not the course's name")

    def test_setName2(self):
        self.courseCS250.setName("NotCS250")
        self.assertEqual("NotCS250", self.courseCS250.courseName, msg="Tried to set the name of the course but "
                                                                      "didn't corrently store the new course name.")

    def test_setName3(self):
        with self.assertRaises(ValidationError, msg="Course name cannot be None"):
            self.courseCS250.setName(None)

    def test_setName4(self):
        with self.assertRaises(ValidationError, msg="Course Name cannot be an Integer"):
            self.courseCS250.setName(1)

    def test_setName5(self):
        with self.assertRaises(ValidationError, msg="Course name cannot be empty"):
            self.courseCS250.setName('')

    # "returned course description was not the course's description"
    def test_getDescription(self):
        description = self.courseCS250.getDescription()
        self.assertEqual("Some elementary comp sci class", description,
                         msg="returned course description was not the course's description")

    def test_setDescription2(self):
        self.courseCS250.setDescription("I love green eggs.")
        self.assertEqual("I love green eggs.", self.courseCS250.courseDescription, msg="course description"
                                                                                       "wasn't set properly.")

    def test_setDescription3(self):
        with self.assertRaises(ValidationError, msg="Description cannot be None"):
            self.courseCS250.setDescription(None)

    def test_setDescription4(self):
        with self.assertRaises(ValidationError, msg="Description cannot be an Integer"):
            self.courseCS250.setDescription(1)

    def test_setDescription5(self):
        with self.assertRaises(ValidationError, msg="Description cannot be empty"):
            self.courseCS250.setDescription('')

    def test_getDepartment(self):
        self.courseCS250.getDepartment()
        self.assertEqual("CS", self.courseCS250.courseDepartment,
                         msg="returned department is not the course's department.")

    def test_setDepartment(self):
        self.courseCS250.setDepartment("yolo")
        self.assertEqual("yolo", self.courseCS250.courseDepartment,
                         msg="department wasn't set properly.")

    def test_setDepartment2(self):
        with self.assertRaises(ValidationError, msg="Department cannot be None"):
            self.courseCS250.setDepartment(None)

    def test_setDepartment3(self):
        with self.assertRaises(ValidationError, msg="Department must be a String type"):
            self.courseCS250.setDepartment(1)

    def test_setDepartment4(self):
        with self.assertRaises(ValidationError, msg="Department cannot be empty"):
            self.courseCS250.setDepartment('')

    # no need for add/remove section, but keeping it here just in case
    # def test_addSection(self):
    #     """ mockSection = Section(1, "England", "1PM", "10PM", 300, User("taemail@uwm.edu", "mypass", "", 3), 2)"""
    #
    #     mockSection = "mock"
    #     self.courseCS350.addSection(mockSection)
    #     self.assertEqual(mockSection, self.courseCS350.Section[0], msg="Added section is not added to the section array"
    #                                                                    "in courses")
    #
    # def test_removeSection(self):
    #     """mockSection = Section(1, "England", "1PM", "10PM", 300, User("taemail@uwm.edu", "mypass", "", 3), 2)"""
    #     mockSection = "mock"
    #     self.courseCS350.addSection(mockSection)
    #     self.courseCS350.removeSection(mockSection.getID())
    #     self.assertEqual(None, self.courseCS350.Section[0],
    #                      msg="Added section is not removed from the section array in "
    #                          "courses")


# formadd, formsave, getcourse, removecourse,getall
# fields = ['courseID', 'courseName', 'courseDescription', 'courseDepartment']
class testFormAdd(TestCase):

    def setUp(self):
        self.form = CourseForm({'courseID': 1, 'courseName': 'Python 101', 'courseDescription':
            'An introductory course to Python', 'courseDepartment': 'CS'})
        self.badFormCourseID = CourseForm({'courseID': '', 'courseName': 'Python 101', 'courseDescription':
            'An introductory course to Python', 'courseDepartment': 'CS'})
        self.badFormCourseName = CourseForm({'courseID': 1, 'courseName': '', 'courseDescription':
            'An introductory course to Python', 'courseDepartment': 'CS'})
        self.badFormCourseDesc = CourseForm({'courseID': 1, 'courseName': 'Python 101', 'courseDescription':
            '', 'courseDepartment': 'CS'})
        self.badFormCourseDept = CourseForm({'courseID': 1, 'courseName': 'Python 101', 'courseDescription':
            'An introductory course to Python', 'courseDepartment': ''})

    def test_addFormGood(self):
        self.assertEqual(Course.formAdd(self.form), True, msg='Form was valid but wasnt added')

    def test_addFormBadID(self):
        self.assertEqual(Course.formAdd(self.badFormCourseID), False, msg="Form was invalid but was added")

    def test_addFormBadID2(self):
        pass

    def test_addFormBadID3(self):
        pass

    def test_addFormBadCourseName(self):
        pass

    def test_addFormBadCourseName2(self):
        pass

    def test_addFormBadCourseName3(self):
        pass

    def test_addFormBadCourseName4(self):
        pass

    def test_addFormBadCourseDesc(self):
        pass

    def test_addFormBadCourseDesc2(self):
        pass

    def test_addFormBadCourseDesc3(self):
        pass

    def test_addFormBadCourseDesc4(self):
        pass

    def test_addFormBadCourseDept(self):
        pass

    def test_addFormBadCourseDept2(self):
        pass

    def test_addFormBadCourseDept3(self):
        pass



class testFormSave(TestCase):
    pass


class testGetCourse(TestCase):
    pass


class testRemoveCourse(TestCase):
    pass


class testGetAll(TestCourse):
    pass
