from django.test import TestCase, Client
from Management.models import Course, UsersToCourse, User
from django.urls import reverse

class Test_UserToCourseAdd(TestCase):
    def setUp(self):
        self.client = Client()
        self.TA1 = User.objects.create(email="SomeUser@user.com", password="testpassword", phone="", role=3)
        self.course1 = Course.objects.create(courseID="1", courseName="CS250",
                                             courseDescription="Some elementary comp sci class", courseDepartment="CS")



        self.userToCourseAddURL = reverse('userToCourseAdd', kwargs={'course_id': self.course1.courseID})

    def test_adding_new_user_to_course(self):
        self.client.post(self.userToCourseAddURL, {
            'assignment': self.TA1
        })

        #checks to see if a usertocourse object is created.
        self.assertEqual(1, UsersToCourse.objects.filter(assignment=self.TA1.email,
                                                         courseID=self.course1.courseID).count(),
                         "user to course object was not created")
    def test_adding_existing_user_to_course(self):
        self.client.post(self.userToCourseAddURL, {
            'assignment': self.TA1
        })
        self.client.post(self.userToCourseAddURL, {
            'assignment': self.TA1
        })

        #checks to see if there is only one object.
        self.assertEqual(1, UsersToCourse.objects.filter(assignment=self.TA1.email,
                                                         courseID=self.course1.courseID).count(),
                         "There are two usertocourseobjects with the same email and courseID")