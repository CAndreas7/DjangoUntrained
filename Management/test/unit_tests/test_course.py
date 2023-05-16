import unittest

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import Http404

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
        self.courseCS250 = Course(4, "CS250", "Some elementary comp sci class", "CS")
        self.courseCS350 = Course(5, "CS350", "Some mediumentary comp sci class", "CS")
        self.courseNotCS = Course(6, "Chemistry 100", "Yuck, some natural science class", "Chemistry")
        self.courseCS250.save()
        self.courseCS350.save()
        self.courseNotCS.save()


    def test_addFormGood(self):
        self.assertEqual(Course.formAdd(self.form), True, msg='Form was valid but wasnt added')

    def test_addFormBadID(self):
        self.assertEqual(Course.formAdd(self.badFormCourseID), False, msg="CourseID was empty but added")

    def test_addFormBadID2(self):
        self.badFormCourseID.courseID = None
        self.assertEqual(Course.formAdd(self.badFormCourseID), False, msg="CourseID cannot be None")

    def test_addFormBadCourseName(self):
        self.assertEqual(Course.formAdd(self.badFormCourseName), False, msg="CourseName was cannot by empty")

    def test_addFormBadCourseName2(self):
        self.badFormCourseName.courseName = None
        self.assertEqual(Course.formAdd(self.badFormCourseName), False, msg="CourseName cannot be None")

    def test_addFormBadCourseName3(self):
        self.badFormCourseName.courseName = 1
        self.assertEqual(Course.formAdd(self.badFormCourseName), False, msg="CourseName cannot be an Integer")

    def test_addFormBadCourseDesc(self):
        self.assertEqual(Course.formAdd(self.badFormCourseDesc), False, msg="CourseDesc cannot be empty")

    def test_addFormBadCourseDesc2(self):
        self.badFormCourseDesc.courseDescription = None
        self.assertEqual(Course.formAdd(self.badFormCourseDesc), False, msg="CourseDesc cannot be None")

    def test_addFormBadCourseDesc3(self):
        self.badFormCourseDesc.courseDescription = 1
        self.assertEqual(Course.formAdd(self.badFormCourseDesc), False, msg="CourseDesc cannot be an Integer")

    def test_addFormBadCourseDept(self):
        self.assertEqual(Course.formAdd(self.badFormCourseDept), False, msg="CourseDept cannot be empty")

    def test_addFormBadCourseDept2(self):
        self.badFormCourseDept.courseDepartment = None
        self.assertEqual(Course.formAdd(self.badFormCourseDept), False, msg="CourseDept cannot be None")

    def test_addFormBadCourseDept3(self):
        self.badFormCourseDept = 1
        self.assertEqual(Course.formAdd(self.badFormCourseDesc), False, msg="CourseDept cannot be an Integer")

    def test_addFormCount(self):
        Course.formAdd(self.form)
        self.assertEqual(Course.objects.all().count(), 4, msg="New course added from form was not in the database")


class testFormSave(TestCase):

    # this test class is a little more difficult to make robust tests
    # This method essentially just calls the in house form.save method
    # so we test for True/False returns
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

    def test_formSaveGood(self):
        self.assertEqual(Course.formSave(self.form), True, msg="The form was valid but was not added")

    def test_formSaveBadCourseID(self):
        self.assertEqual(Course.formSave(self.badFormCourseID), False,
                         msg="The form had an empty courseID but was added")

    def test_formSaveBadCourseID2(self):
        self.badFormCourseID.courseID = None
        self.assertEqual(Course.formSave(self.badFormCourseID), False, msg="The form had a None courseID but was added")

    def test_formSaveBadCourseName(self):
        self.assertEqual(Course.formSave(self.badFormCourseName), False, msg="The form had an empty name but was added")

    def test_formSaveBadCourseName2(self):
        self.badFormCourseName.courseName = None
        self.assertEqual(Course.formSave(self.badFormCourseName), False, msg="The form had a None name but was added")

    def test_formSaveBadCourseName3(self):
        self.badFormCourseName.courseName = 1
        self.assertEqual(Course.formSave(self.badFormCourseName), False,
                         msg="The form had an Integer course name but was added")

    def test_formSaveBadCourseDesc(self):
        self.assertEqual(Course.formSave(self.badFormCourseDesc), False,
                         msg="The form had an empty description but was added")

    def test_formSaveBadCourseDesc2(self):
        self.badFormCourseDesc.courseDescription = None
        self.assertEqual(Course.formSave(self.badFormCourseDesc), False,
                         msg="The form had a None description but was added")

    def test_formSaveBadCourseDesc3(self):
        self.badFormCourseDesc.courseDescription = 1
        self.assertEqual(Course.formSave(self.badFormCourseDesc), False,
                         msg="The form had an Integer description but was added")

    def test_badFormCourseDept(self):
        self.assertEqual(Course.formSave(self.badFormCourseDept), False,
                         msg="The form had an Empty department but was added")

    def test_badFormCourseDept2(self):
        self.badFormCourseDept.courseDepartment = None
        self.assertEqual(Course.formSave(self.badFormCourseDept), False,
                         msg="The form had a None department but was added")

    def test_badFormCourseDept3(self):
        self.badFormCourseDept.courseDepartment = 1
        self.assertEqual(Course.formSave(self.badFormCourseDept), False,
                         msg="The form had an Integer department but was added")


# simple test class about a get method or return a 404
class testGetCourse(TestCase):

    def setUp(self):
        self.courseCS250 = Course(1, "CS250", "Some elementary comp sci class", "CS")
        self.courseCS350 = Course(2, "CS350", "Some mediumentary comp sci class", "CS")
        self.courseNotCS = Course(3, "Chemistry 100", "Yuck, some natural science class", "Chemistry")
        self.courseCS250.save()
        self.courseCS350.save()
        self.courseNotCS.save()

    def test_getCourseGood(self):
        self.assertEqual(Course.getCourse(1), self.courseCS250,
                         msg="The given courseID exists but did not grab the correct object")

    def test_getCourseBad(self):
        with self.assertRaises(Http404, msg="Should raise 404 on a user that doesnt exist, but does not"):
            Course.getCourse(42)

    def test_getDeleteCourse(self):
        self.courseCS250.delete()
        with self.assertRaises(Http404, msg="Should raise 404 on a user that doesn't exist, but does not"):
            Course.getCourse(1)


class testRemoveCourse(TestCase):

    def setUp(self):
        self.courseCS250 = Course(1, "CS250", "Some elementary comp sci class", "CS")
        self.courseCS350 = Course(2, "CS350", "Some mediumentary comp sci class", "CS")
        self.courseNotCS = Course(3, "Chemistry 100", "Yuck, some natural science class", "Chemistry")
        self.courseCS250.save()
        self.courseCS350.save()
        self.courseNotCS.save()

    def test_removeCourseGood(self):
        self.courseCS250.removeCourse()
        self.assertEqual(Course.objects.filter(courseID=1).count(), 0,
                         msg="Course was deleted, but is still in the database")

    def test_removeCourseNonExistent(self):
        self.courseCS250.removeCourse()
        # calling remove again on the same object to get something that doesn't exist
        with self.assertRaises(ObjectDoesNotExist, msg="Course does not exist, but did not raise DoesNotExist"):
            self.courseCS250.removeCourse()


class testGetAll(TestCase):

    def setUp(self):
        self.courseCS250 = Course(1, "CS250", "Some elementary comp sci class", "CS")
        self.courseCS350 = Course(2, "CS350", "Some mediumentary comp sci class", "CS")
        self.courseNotCS = Course(3, "Chemistry 100", "Yuck, some natural science class", "Chemistry")
        self.courseCS250.save()
        self.courseCS350.save()
        self.courseNotCS.save()

    def test_getAll(self):
        self.assertEqual(Course.getAll().count(), 3,
                         msg="Number of courses returned does not match number in the Database")

    def test_getAllDeleted(self):
        self.courseCS250.removeCourse()
        self.assertEqual(Course.getAll().count(), 2, msg="A deleted course remained in the database")

    def test_getAllAdded(self):
        form = CourseForm({'courseID': 4, 'courseName': 'Python 101', 'courseDescription':
            'An introductory course to Python', 'courseDepartment': 'CS'})
        Course.formAdd(form)
        self.assertEqual(Course.getAll().count(), 4, msg="Added course was not in the database")
