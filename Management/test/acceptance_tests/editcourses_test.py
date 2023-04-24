from django.test import TestCase, Client
from Management.models import Course


class Test_EditCourses(TestCase):

    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(courseID="1", courseName="CS250",
                                            courseDescription="Some elementary comp sci class", courseDepartment="CS")

    def test_editCourseName(self):
        self.client.post('/courseEdit', courseID=1, courseName="CS001")

        self.assertEqual(Course.objects.filter(courseName="CS001").count(), 1,
                         msg="the course name of CS250 was not changed to CS001")
        self.assertEqual(len(Course.objects.all()), 1, "There should be a total of 1 course in the database.")

    def test_editCourseDescription(self):
        self.client.post('/courseEdit', courseID=1, courseDescription="Actually, this is advanced CS lmao")

        self.assertEqual(Course.objects.filter(courseDescription="Actually, this is advanced CS lmao").count(), 1,
                         msg="the course description was not changed/")
        self.assertEqual(len(Course.objects.all()), 1, "There should STILL be a total of 1 course in the database.")

    def test_editCourseDepartment(self):
        self.client.post('/courseEdit', courseID=1, courseDepartment="Chem.. Yuck")

        self.assertEqual(Course.objects.filter(courseDepartment="Chem.. Yuck").count(), 1,
                         msg="When posting a new course Department field, the course department field was not changed")
        self.assertEqual(len(Course.objects.all()), 1, "There should STILL be a total of 1 course in the database.")

    def test_editNonExistentCourse(self):
        self.client.post('/courseEdit', courseID=500, courseDepartment="Chem.. Yuck")

        self.assertEqual(Course.objects.filter(courseID=500).count(), 0,
                         msg="When posting a new course Department field, the course department field was not changed")
        self.assertEqual(len(Course.objects.all()), 1, "There should STILL be a total of 1 course in the database.")

