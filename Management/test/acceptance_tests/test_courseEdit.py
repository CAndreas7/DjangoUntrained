from django.test import TestCase, Client
from django.urls import reverse
from Management.models import Course


class Test_EditCourses(TestCase):

    def setUp(self):
        self.client = Client()

        # creating a session?
        self.session = self.client.session
        self.session['roleSession'] = 1
        self.session.save()

        self.course = Course.objects.create(courseID=1, courseName="CS250",
                                            courseDescription="Some elementary comp sci class", courseDepartment="CS")
        self.editURL = reverse('courseEdit', kwargs={'course_id': self.course.courseID})


    def test_editCourseName(self):
        response = self.client.post(self.editURL, {
            'courseName': 'CS001',
            'courseDescription': "Some elementary comp sci class",
            'courseDepartment': "CS",
        })

        self.assertEqual("CS001", Course.objects.get(courseID=1).courseName,
                         msg="the course name of CS250 was not changed to CS001")
        self.assertEqual(len(Course.objects.all()), 1, "There should be a total of 1 course in the database.")
        self.assertEqual(response.context['message'], "Course was successfully edited.",
                         "message displayed was not correct")

    def test_editCourseDescription(self):
        response = self.client.post(self.editURL, {
            'courseName': 'CS250',
            'courseDescription': "Some other",
            'courseDepartment': "CS",
        })

        self.assertEqual("Some other", Course.objects.get(courseID=1).courseDescription,
                         "the course description was not changed")
        self.assertEqual(len(Course.objects.all()), 1, "There should STILL be a total of 1 course in the database.")
        self.assertEqual(response.context['message'], "Course was successfully edited.",
                         "message displayed was not correct")

    def test_editCourseDepartment(self):
        response = self.client.post(self.editURL, {
            'courseName': 'CS250',
            'courseDescription': "Chem.. Yuck",
            'courseDepartment': "Not CS",
        })

        self.assertEqual("Not CS", Course.objects.get(courseID=1).courseDepartment,
                         msg="When posting a new course Department field, the course department field was not changed")

        self.assertEqual(len(Course.objects.all()), 1, "There should STILL be a total of 1 course in the database.")
        self.assertEqual(response.context['message'], "Course was successfully edited.",
                         "message displayed was not correct")


