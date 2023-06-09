from django.test import TestCase, Client
from Management.models import Course, UsersToCourse, User
from django.urls import reverse

class Test_UserToCourseAdd(TestCase):
    def setUp(self):
        self.client = Client()
        # creating a session?
        self.session = self.client.session
        self.session['roleSession'] = 1
        self.session.save()

        self.TA1 = User.objects.create(email="SomeUser@user.com", password="testpassword", phone="", role=3)
        self.course1 = Course.objects.create(courseID=1, courseName="CS250",
                                             courseDescription="Some elementary comp sci class", courseDepartment="CS")
        self.course2 = Course.objects.create(courseID=2, courseName="CS250",
                                             courseDescription="Some elementary comp sci class", courseDepartment="CS")

        self.instr = User.objects.create(email="inst@inst.com", password="testpassword", phone="", role=2)


        self.userToCourseAddURL = reverse('userToCourseAdd', kwargs={'course_id': self.course1.courseID})

        self.userToCourse2AddURL = reverse('userToCourseAdd', kwargs={'course_id': self.course2.courseID})

    def test_user_add_themselves_to_course(self):
        self.session['roleSession'] = 2
        response = self.client.post(self.userToCourseAddURL, {
            'Assignment': "inst@inst.com"
        })

        self.assertEqual(response.context['message'], "User successfully added to course.")

    def test_user_add_themselves_to_unassigned_course(self):
        self.session['roleSession'] = 2
        response = self.client.post(self.userToCourse2AddURL, {
            'Assignment': "inst@inst.com"
        })

        self.assertEqual(response.context['message'], "User is not assigned to this course by the supervisor")

    def test_adding_new_user_to_course(self):
        response = self.client.post(self.userToCourseAddURL, {
            'Assignment': self.TA1.email
        })

        #checks to see if a usertocourse object is created.
        self.assertEqual(1, UsersToCourse.objects.filter(assignment=self.TA1.email,
                                                         courseID=self.course1.courseID).count(),
                         "user to course object was not created")
    def test_adding_existing_user_to_course(self):
        self.client.post(self.userToCourseAddURL, {
            'Assignment': self.TA1.email
        })
        self.client.post(self.userToCourseAddURL, {
            'Assignment': self.TA1.email
        })

        #checks to see if there is only one object.
        self.assertEqual(1, UsersToCourse.objects.filter(assignment=self.TA1.email,
                                                         courseID=self.course1.courseID).count(),
                         "There are two usertocourseobjects with the same email and courseID")