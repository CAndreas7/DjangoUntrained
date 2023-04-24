from django.test import TestCase, Client
from Management.models import Course

class Test_AddRemoveCourses(TestCase):
    def setUp(self):

        self.client = Client()

        self.course = Course.objects.create(courseID="1", courseName="CS250",
                                            courseDescription="Some elementary comp sci class", courseDepartment="CS")
        self.course.save()

        self.client.post('/courseAdd', {
            'courseID': '2',
            'courseName': 'CS350',
            'courseDescription': "Some elementary comp sci class",
            'courseDepartment': "CS"
        })

    def test_addNewCourse(self):
        self.client.post('/courseAdd', {
            'courseID': '3',
            'courseName': 'CS400',
            'courseDescription': "Some elementary comp sci class",
            'courseDepartment': "CS"
        })
        self.assertEqual(Course.objects.filter(courseID=2).count(), 1,
                         msg="the new course should have been added to the database ")
        self.assertEqual(len(Course.objects.all()), 3, "There should be a total of 3 courses in the database.")

    def test_addSameCourse(self):
        self.client.post('/courseAdd', {
            'courseID': '1',
            'courseName': 'CS250',
            'courseDescription': "Some elementary comp sci class",
            'courseDepartment': "CS"
        })

        self.assertEqual(Course.objects.filter(courseID=1).count(), 2, msg= "there should not be two same courses in the "
                                                                           "data base")
        self.assertEqual(len(Course.objects.all()), 2, "There should be a total of 2 courses in the database.")
    def test_addSameID(self):
        self.client.post('/courseAdd', {
            'courseID': '1',
            'courseName': 'CS550',
            'courseDescription': "Some elementary comp sci class",
            'courseDepartment': "CS"
        })
        self.assertEqual(Course.objects.filter(courseID=1).count(), 1,
                         msg="there should not be two same courses with identical IDs in the "
                             "data base")
        self.assertEqual(len(Course.objects.all()), 2, "There should be a total of 2 courses in the database.")

    def test_addSameCourseName(self):
        self.client.post('/courseAdd', {
            'courseID': '5',
            'courseName': 'CS200',
            'courseDescription': "Some elementary comp sci class",
            'courseDepartment': "CS"
        })
        self.assertEqual(Course.objects.filter(courseID=1).count(), 1,
                         msg="there should not be two same courses with identical courseNames in the "
                             "data base")
        self.assertEqual(len(Course.objects.all()), 2, "There should be a total of 2 courses in the database.")

    def test_removeExistingCourse(self):
        """I'm assuming we do a post method on the button to remove the course from the database. I'll wait until
        it is implemented before writing this."""
        pass

    def test_removeNonExistingCourse(self):
        pass