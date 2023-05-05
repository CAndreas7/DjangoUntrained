from django.core.exceptions import ObjectDoesNotExist
from Management.models import User, Course, UsersToCourse
from django.test import TestCase
class TestUsersToCourse(TestCase):
    def setUp(self):
        self.supervisor = User("supervisor@uwm.edu", "Visor", "Super", "superpassword", "", 1)
        self.taOld = User("taOld@uwm.edu", "Wayne", "Bruce", "taOldpassword", "", 3)
        self.taOld.save()
        self.taNew = User("taNew@uwm.edu", "Kent", 'Clark' "taNewpassword", "", 3)
        self.courseCS911 = Course(911, "CS911", "Emergency computer science, enroll immediately.", "CS")
        self.courseCS911.save()
        self.courseMUS001 = Course(1, "MUS001", "Just like a wartime novelty.", "MUS")
        self.courseMUS001.save()
        self.usersToCourse01 = UsersToCourse(assignment=self.taOld.email, courseID=self.courseCS911.courseID)
        self.usersToCourse01.save()




    def test_getUserPass(self):
        user = self.usersToCourse01.getUser()
        self.assertEqual(user, self.taOld, msg="Returned user not the same as assigned user.")


    def test_getCoursePass(self):
        course = self.usersToCourse01.getCourse()
        self.assertEqual(course, self.courseCS911, msg="Returned course not the same as assigned course.")


    def test_removeUserPass(self):
        self.usersToCourse01.removeUser()
        self.assertEqual(UsersToCourse.objects.filter(assignment=self.taOld.email, courseID=self.courseCS911.courseID).count(), 0,
                         msg="A record exists with the primary key that should have been deleted")
