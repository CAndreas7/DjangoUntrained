from django.core.exceptions import ObjectDoesNotExist

from Management.models import User, Course, UsersToCourse
from django.test import TestCase


class TestUsersToCourse(TestCase):

    def setUp(self):
        self.supervisor = User("supervisor@uwm.edu", "superpassword", "", 1)
        self.taOld = User("taOld@uwm.edu", "taOldpassword", "", 3)
        self.taNew = User("taNew@uwm.edu", "taNewpassword", "", 3)
        self.courseCS911 = Course(911, "CS911", "Emergency computer science, enroll immediately.", "CS")
        self.courseCS911.save()
        self.courseMUS001 = Course(1, "MUS001", "Just like a wartime novelty.", "MUS")
        self.courseMUS001.save()
        self.usersToCourse01 = UsersToCourse(assignment=self.taOld, courseID=self.courseCS911)
        self.usersToCourse02 = UsersToCourse(assignment=self.taOld, courseID=self.courseCS911)

    def test_getUser(self):
        user = self.usersToCourse01.getUser()
        self.assertEqual(user, self.usersToCourse01.assignment, msg="Returned user not the same as assigned user.")

    def test_getCourse(self):
        course = self.usersToCourse01.getCourse()
        self.assertEqual(course, self.usersToCourse01.courseID, msg="Returned course not the same as assigned course.")

    def test_setUser_Name(self):
        self.usersToCourse01.setUser_Name(self.taNew)
        self.assertEqual(self.usersToCourse01.assignment, self.taNew, msg="User not correctly assigned to course.")

    def test_setCourseName(self):
        self.usersToCourse01.setCourseName(self.courseMUS001)
        self.assertEqual(self.usersToCourse01.courseID, self.courseMUS001, msg="Course not correctly assigned to user.")

    # Need to implement Course.removeCourse() for this to work
    # def test_removeCourse(self):
    #     self.courseMUS001.removeCourse(1)
    #     self.assertIsNone(self.usersToCourse01, msg="Deleting a course failed to delete the usersToCourse junction.")
    # Need to implement User.removeUser for this to work.
    # def test_removeUser(self):
    #     self.supervisor.removeAccount(self.taOld.email)
    #     self.assertIsNone(self.usersToCourse02, msg="Deleting a user failed to delete the usersToCourse junction.")

    # def test_removeUser(self):
    #     test_uTc_id = self.usersToCourse02.id
    #     # self.supervisor.removeAccount(self.taOld.email)
    # with self.assertRaises(ObjectDoesNotExist, msg="Denominator of zero fails to raise DivByZero"):
    #     test_uTc =
    #     with self.assertRaises(UsersToCourse.DoesNotExist, msg="Deleting user did not remove junction."):
    #         UsersToCourse.objects.get(id=test_uTc_id)

