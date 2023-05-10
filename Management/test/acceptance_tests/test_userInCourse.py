from django.test import TestCase, Client
from Management.models import Course, UsersToCourse, User
from django.urls import reverse

class Test_UserInCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.TA1 = User.objects.create(email="SomeUser@user.com", password="testpassword", phone="", role=3)
        self.course1 = Course.objects.create(courseID="1", courseName="CS250",
                                             courseDescription="Some elementary comp sci class", courseDepartment="CS")

        self.TA1toCourse1 = UsersToCourse.objects.create(assignment=self.TA1.email, courseID=self.course1.courseID)

        self.addUserToCourseURL = reverse('userToCourseAdd', kwargs={'course_id': self.course1.courseID})
        self.deleteUserInCourseURL = reverse('userToCourseDelete', kwargs={'email_id': self.TA1.email,
                                                                    'course_id': self.course1.courseID})

    def test_add_user_link(self):
        response = self.client.get(self.addUserToCourseURL)

        self.assertEqual(response.status_code, 200, "response status code is not 200")

    def test_remove_user_from_course(self):
        response = self.client.get(self.deleteUserInCourseURL)

        #checks to see if the user to course object is deleted.
        self.assertEqual(0, UsersToCourse.objects.filter(assignment=self.TA1.email,
                                                         courseID=self.course1.courseID).count(),
                         "userToCourse object was not deleted from the junction table.")

        #checks to see if the user was deleted.
        self.assertEqual(1, User.objects.filter(email=self.TA1.email).count(),
                         "User object was deleted when it shouldn't have been.")
        #checks to see if the course was deleted.
        self.assertEqual(1, Course.objects.filter(courseID=self.course1.courseID).count(),
                         "Course object was deleted when it shouldn't have been")
