from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse

from Management.forms import SectionForm
from Management.models import Course, Section, User
from Management.views import sections, sectionAdd, sectionEdit, sectionDelete, courses


class testSections(TestCase):
    def setUp(self):
        self.taOld = User(email="taOld@uwm.edu", lName="test", fName="Unit", password="taOldpassword", phone="", role=3)
        self.taNew = User(email="taNew@uwm.edu", lName="Vendor", fName="Fruit", password="taNewpassword", phone="",
                          role=3)
        self.courseMUS001 = Course(1, "MUS001", "Just like a wartime novelty.", "MUS")
        self.courseCS911 = Course(911, "CS911", "Emergency computer science, enroll immediately.", "CS")
        self.section001 = Section(sectionID=1, location="Backyard", startTime="12:00PM", endTime="12:01PM", capacity=30,
                                  TA=self.taOld, courseID=self.courseMUS001)
        self.taOld.save()
        self.taNew.save()
        self.courseMUS001.save()
        self.courseCS911.save()
        self.section001.save()

    def test_getID(self):
        self.assertEqual(self.section001.getID(), 1, msg="This should return 1, but did not")

    def test_getID2(self):
        tempSectionID = self.section001.getID()
        self.assertEqual(tempSectionID, self.section001.sectionID,
                         msg="getSectionID did not return the correct sectionID")
        # response = self.client.get(reverse('sections', args=[self.course.courseID]))
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'main/sections.html')
        # self.assertContains(response, 'Test Course')
        # self.assertContains(response, '1')

    def test_getLocation(self):
        tempLocation = self.section001.getLocation()
        self.assertEqual(tempLocation, self.section001.location,
                         msg="getSectionLocation did not return the correct location")

    def test_setLocation(self):
        self.section001.setLocation("MUS150")
        self.assertEqual("MUS150", self.section001.location, msg="setSectionLocation did not work correctly")

    def test_setLocation2(self):
        with self.assertRaises(ValidationError, msg="Location cannot be None"):
            self.section001.setLocation(None)

    def test_setLocation3(self):
        with self.assertRaises(ValidationError, msg="Location must be an Integer"):
            self.section001.setLocation(1)

    def test_setLocation4(self):
        with self.assertRaises(ValidationError, msg="Location cannot be empty"):
            self.section001.setLocation("")

    def test_getStart(self):
        tempStart = self.section001.getStart()
        self.assertEqual(tempStart, self.section001.startTime,
                         msg="getSectionStart did not return the correct start time")

    def test_setStart(self):
        self.section001.setStart("12:00AM")
        self.assertEqual("12:00AM", self.section001.startTime, msg="setSectionStart did not work correctly")

    def test_setStart2(self):
        with self.assertRaises(ValidationError, msg="Start Time cannot be None"):
            self.section001.setStart(None)

    def test_setStart(self):
        with self.assertRaises(ValidationError, msg="Start Time must be a String"):
            self.section001.setStart(1)

    def test_setStart4(self):
        with self.assertRaises(ValidationError, msg="Start Time cannot be empty"):
            self.section001.setStart("")

    def test_getEnd(self):
        tempEnd = self.section001.getEnd()
        self.assertEqual(tempEnd, self.section001.endTime, msg="getSectionEnd did not return the correct end time")

    def test_setEnd(self):
        self.section001.setEnd("12:01AM")
        self.assertEqual("12:01AM", self.section001.endTime, msg="setSectionEnd did not work correctly")

    def test_setEnd2(self):
        with self.assertRaises(ValidationError, msg="End Time cannot be None"):
            self.section001.setEnd(None)

    def test_setEnd3(self):
        with self.assertRaises(ValidationError, msg="End Time must be a String"):
            self.section001.setEnd(1)

    def test_setEnd4(self):
        with self.assertRaises(ValidationError, msg="End Time cannot be empty"):
            self.section001.setEnd("")

    def test_getCapacity(self):
        capacity = self.section001.getCapacity()
        self.assertEqual(capacity, self.section001.capacity, msg="getCapacity did not return the correct capacity")

    def test_setCapacity(self):
        self.section001.setCapacity(1)
        self.assertEqual(1, self.section001.capacity, msg="setCapacity did not work correctly")

    def test_setCapacity2(self):
        with self.assertRaises(ValidationError, msg="Capacity cannot be None"):
            self.section001.setCapacity(None)

    def test_setCapacity3(self):
        with self.assertRaises(ValidationError, msg="Capacity must be an Integer"):
            self.section001.setCapacity("")

    def test_setCapacity4(self):
        with self.assertRaises(ValidationError, msg="Capacity cannot be negative"):
            self.section001.setCapacity(-1)

    def test_getTA(self):
        TA = self.section001.getTA()
        self.assertEqual(TA, self.section001.TA, msg="getTA did not return the correct TA")

    def test_setTA(self):
        self.section001.setTA(self.taNew)
        self.assertEqual(self.taNew, self.section001.TA, msg="setTA did not work correctly")

    def test_setTA2(self):
        with self.assertRaises(ValidationError, msg="The TA parameter must be a User object"):
            self.section001.setTA(self.courseCS911)

    def test_setTA3(self):
        # fakeTA = User(email="fake@uwm.edu", lName="Real", fName="Not", password="fakeman", phone="867-5309", role=3)
        # fakeTA.delete()
        self.taNew.delete()
        with self.assertRaises(ObjectDoesNotExist, msg="You cannot add a TA that is not in the database"):
            self.section001.setTA(self.taNew)

    def test_getCourseID(self):
        courseID = self.section001.getCourseID()
        self.assertEqual(courseID, self.section001.courseID, msg="getCourseID did not return the correct course ID")

    def test_setCourseID(self):
        self.section001.setCourseID(self.courseCS911)
        self.assertEqual(self.courseCS911, self.section001.courseID, msg="setCourseID did not work correctly")

    def test_setCourseID2(self):
        with self.assertRaises(ValidationError, msg="Course must be a Course Object"):
            self.section001.setCourseID(self.taNew)

    def test_setCourseID3(self):
        self.courseMUS001.delete()
        with self.assertRaises(ObjectDoesNotExist, msg="Course must exist in the database"):
            self.section001.setCourseID(self.courseMUS001)


class testGetSectionsFromCourse(TestCase):

    def setUp(self):
        self.taOld = User(email="taOld@uwm.edu", lName="test", fName="Unit", password="taOldpassword", phone="", role=3)
        self.taNew = User(email="taNew@uwm.edu", lName="Vendor", fName="Fruit", password="taNewpassword", phone="",
                          role=3)
        self.courseMUS001 = Course(1, "MUS001", "Just like a wartime novelty.", "MUS")
        self.courseCS911 = Course(911, "CS911", "Emergency computer science, enroll immediately.", "CS")
        self.section001 = Section(sectionID=1, location="Backyard", startTime="12:00PM", endTime="12:01PM", capacity=30,
                                  TA=self.taOld, courseID=self.courseMUS001)
        self.taOld.save()
        self.taNew.save()
        self.courseMUS001.save()
        self.courseCS911.save()
        self.section001.save()

    def test_getSectionFromCourseGood(self):
        self.assertEqual(Section.getSectionsFromCourse(self.courseMUS001.courseID).count(), 1,
                         msg="Only one section in the course")

    def test_getSectionFromCourseEmpty(self):
        self.assertEqual(Section.getSectionsFromCourse(self.courseCS911.courseID).count(), 0,
                         msg="Did not return empty queryset")

    def test_getSectionFromCourseBad(self):
        fakeCourse = Course(courseID=87, courseName="Not real", courseDescription="This course is fake, nerd",
                            courseDepartment="Imaginary")
        with self.assertRaises(ObjectDoesNotExist, msg="This course is not in the database"):
            Section.getSectionsFromCourse(fakeCourse.courseID)


class testFormAdd(TestCase):
    # fields = ['sectionID', 'location', 'startTime', 'endTime', 'capacity', 'TA']
    def setUp(self):
        self.taOld = User(email="taOld@uwm.edu", lName="test", fName="Unit", password="taOldpassword", phone="", role=3)
        self.courseMUS001 = Course(1, "MUS001", "Just like a wartime novelty.", "MUS")
        self.taOld.save()
        self.courseMUS001.save()
        self.form = SectionForm({"sectionID": 1, "location": "CHEM190", "startTime": "09:30AM", "endTime": "10:20AM",
                                 "capacity": 80, "TA": self.taOld})
        self.badFormSID = SectionForm(
            {"sectionID": "a", "location": "CHEM190", "startTime": "09:30AM", "endTime": "10:20AM",
             "capacity": 80, "TA": self.taOld})
        self.badFormLoc = SectionForm(
            {"sectionID": 1, "location": "", "startTime": "09:30AM", "endTime": "10:20AM",
             "capacity": 80, "TA": self.taOld})
        self.badFormStart = SectionForm({"sectionID": 1, "location": "CHEM190", "startTime": "", "endTime": "10:20AM",
                                         "capacity": 80, "TA": self.taOld})
        self.badFormEnd = SectionForm({"sectionID": 1, "location": "CHEM190", "startTime": "09:30AM", "endTime": "",
                                 "capacity": 80, "TA": self.taOld})
        self.form = SectionForm({"sectionID": 1, "location": "CHEM190", "startTime": "09:30AM", "endTime": "10:20AM",
                                 "capacity": 80, "TA": self.taOld})

    def test_formAddGood(self):
        self.assertEqual(Section.formAdd(self.form, self.courseMUS001.courseID), True,
                         msg="The form is valid but was not added")

    def test_formAddBadSID(self):
        self.assertEqual(Section.formAdd(self.form, self.courseMUS001.courseID), False,
                         msg="The form had an invalid sectionID but added")

    def test_formAddBadLoc(self):
        self.form.location = ""
        self.assertEqual(Section.formAdd(self.badFormLoc, self.courseMUS001.courseID), False,
                         msg="The form had an invalid location but was added")

    def test_formAddBadStart(self):
        self.form.startTime = ""
        self.assertEqual(Section.formAdd(self.badFormStart, self.courseMUS001.courseID), False,
                         msg="The form had an invalid start time but was added")

    def test_formAddBadEnd(self):
        self.form.endTime = ""
        self.assertEqual(Section.formAdd(self.form, self.courseMUS001.courseID), False,
                         msg="The form had an invalid end time but was added")

    def test_formAddBadCapacity(self):
        self.form.capacity = "a"
        self.assertEqual(Section.formAdd(self.form, self.courseMUS001.courseID), False,
                         msg="The form had an invalid capacity but was added")

    def test_formAddBadTA(self):
        self.form.TA = "a"
        self.assertEqual(Section.formAdd(self.form, self.courseMUS001.courseID), False,
                         msg="The form had an invalid TA but was added anyways")

    def test_formAddBadCourse(self):
        with self.assertRaises(ObjectDoesNotExist, msg="The given courseID must correspond to a course in the system"):
            Section.formAdd(self.form, 9)


class testFormSave(TestCase):
    pass


class testGetSection(TestCase):
    pass


class testDeleteSection(TestCase):
    pass
