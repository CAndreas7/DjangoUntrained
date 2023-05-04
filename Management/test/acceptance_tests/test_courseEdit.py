from django.test import TestCase, Client
from Management.models import Course


class Test_EditCourses(TestCase):

    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(courseID=1, courseName="CS250",
                                            courseDescription="Some elementary comp sci class", courseDepartment="CS")

    def test_editCourseName(self):
        self.client.post('/courseEdit/', {
            'courseID': 1,
            'courseName': 'CS001',
            'courseDescription': "Some elementary comp sci class",
            'courseDepartment': "CS",
        })

        self.assertEqual("CS001", Course.objects.get(courseID=1).courseName,
                         msg="the course name of CS250 was not changed to CS001")
        self.assertEqual(len(Course.objects.all()), 1, "There should be a total of 1 course in the database.")

    def test_editCourseDescription(self):
        self.client.post('/courseEdit/', {
            'courseID': 1,
            'courseName': 'CS250',
            'courseDescription': "Some other",
            'courseDepartment': "CS",
        })

        self.assertEqual("Some other", Course.objects.get(courseID=1).courseDescription,
                         "the course description was not changed")
        self.assertEqual(len(Course.objects.all()), 1, "There should STILL be a total of 1 course in the database.")

    def test_editCourseDepartment(self):
        self.client.post('/courseEdit/', {
            'courseID': 1,
            'courseName': 'CS250',
            'courseDescription': "Chem.. Yuck",
            'courseDepartment': "Not CS",
        }, 1)

        self.assertEqual("Not CS", Course.objects.get(courseID=1).courseDepartment,
                         msg="When posting a new course Department field, the course department field was not changed")

        self.assertEqual(len(Course.objects.all()), 1, "There should STILL be a total of 1 course in the database.")


