from django.core.exceptions import ObjectDoesNotExist
from Management.models import User, Course, UsersToCourse
from django.test import TestCase


class TestUsersToCourse(TestCase):
    def setUp(self):
        self.supervisor = User("supervisor@uwm.edu", "Visor", "Super", "superpassword", "", 1)
        self.taOld = User("taOld@uwm.edu", "Wayne", "Bruce", "taOldpassword", "", 3)
        self.taOld.save()
        self.taNew = User("taNew@uwm.edu", "Kent", "Clark", "taNewpassword", "", 3)
        self.taNew.save()
        self.courseCS911 = Course(911, "CS911", "Emergency computer science, enroll immediately.", "CS")
        self.courseCS911.save()
        self.courseMUS001 = Course(1, "MUS001", "Just like a wartime novelty.", "MUS")
        self.courseMUS001.save()
        self.usersToCourse01 = UsersToCourse(assignment=self.taOld.email, courseID=self.courseCS911.courseID)
        self.usersToCourse01.save()
        self.usersToCourse02 = UsersToCourse(assignment=self.taNew.email, courseID=self.courseMUS001.courseID)
        self.usersToCourse02.save()

    def test_getUserPass(self):
        user = self.usersToCourse01.getUser()
        self.assertEqual(user, self.taOld, msg="Returned user not the same as assigned user.")

    def test_getCoursePass(self):
        course = self.usersToCourse01.getCourse()
        self.assertEqual(course, self.courseCS911, msg="Returned course not the same as assigned course.")

    def test_getUserToCourse(self):
        courseUsers = UsersToCourse.getUserInCourse(911)
        self.assertQuerysetEqual(courseUsers, UsersToCourse.objects.filter(courseID=911),
                                 msg="getUserToCourse did not return the correct users assigned to the course.")

    def test_getUserCourses(self):
        courseUsers = UsersToCourse.getUserCourses(self.taOld.email)
        self.assertQuerysetEqual(courseUsers, UsersToCourse.objects.filter(assignment=self.taOld.email),
                                 msg="getUserToCourse did not return the correct users assigned to the course.")

    def test_addUserToCourse(self):
        newUtcObject = UsersToCourse.addUserToCourse(self.taNew.email, self.courseMUS001.courseID)
        self.assertIn(newUtcObject, UsersToCourse.objects.all(),
                      msg="The user was not successfully added to the course.")

    def test_delCourseUsers(self):
        UsersToCourse.delCourseUsers(self.courseMUS001.courseID)
        self.assertEqual(0, UsersToCourse.objects.filter(courseID=self.courseMUS001.courseID).count(),
                         msg="Objects still exist assigning users to this course.")

    def test_delUserCourses(self):
        UsersToCourse.delUserCourses(self.taOld.email)
        self.assertEqual(0, UsersToCourse.objects.filter(assignment=self.taOld.email).count(),
                         msg="Objects still exist with this user assigned to courses.")

    def test_removePairing(self):
        self.usersToCourse01.removePairing()
        self.assertEqual(UsersToCourse.objects.filter().count(), 1, msg="There can only be one")
