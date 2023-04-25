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
            'courseID': '1236',
            'courseName': 'CS400',
            'courseDescription': "Some elementary comp sci class",
            'courseDepartment': "CS"
        })
        response = self.client.get('/courseAdd')

        #self.assertEqual(200, response.status_code, "Status code is not 200")

        # Checks to see if post method correctly adds courses to the database.
        self.assertEqual(Course.objects.filter(courseID=1236).count(), 1,
                         msg="the new course should have been added to the database ")
        self.assertEqual(len(Course.objects.all()), 3, "There should be a total of 3 courses in the database.")

        # checks to see if the website prints correct response contents.
        self.assertNotIn(response.content, 'Please fill out this field.', msg="Response displayed the adding"
                                                                      "\"the same course\"error message, when it "
                                                                      "shouldn't have");
        self.assertIn(response.content, 'course added successfully', msg="response did not show the correct message for"
                                                                         "adding a course successfully.")

    def test_addSameCourse(self):
        self.client.post('/courseAdd', {
            'courseID': '1',
            'courseName': 'CS250',
            'courseDescription': "Some elementary comp sci class",
            'courseDepartment': "CS"
        })
        """Checks to see if the course is correctly added to the database via post"""
        self.assertEqual(Course.objects.filter(courseID=1).count(), 2,
                         msg="there should not be two same courses in the "
                             "data base")
        self.assertEqual(len(Course.objects.all()), 2, "There should be a total of 2 courses in the database.")
        """Checks to see if correct message displays """
        response = self.client.get('/courseAdd')
        self.assertIn(response.content, "Cannot add same course", msg="Response didn't correctly display the adding"
                                                                      "\"the same course\"error message");

    def test_addSameID(self):
        self.client.post('/courseAdd', {
            'courseID': '1',
            'courseName': 'CS550',
            'courseDescription': "Some elementary comp sci class",
            'courseDepartment': "CS"
        })
        # Checks to see if post method correctly adds courses to the database.
        self.assertEqual(Course.objects.filter(courseID=1).count(), 1,
                         msg="there should not be two same courses with identical IDs in the "
                             "data base")
        self.assertEqual(len(Course.objects.all()), 2, "There should be a total of 2 courses in the database.")

        # checks to see if correct message is displayed when trying to add a course with the same ID.
        response = self.client.get('/courseAdd')
        self.assertIn(response.content, "Cannot add a course with an ID in the system",
                      msg="Response didn't correctly display the adding"
                          "\"the same ID\"error message");

    def test_addSameCourseName(self):
        self.client.post('/courseAdd', {
            'courseID': '5',
            'courseName': 'CS200',
            'courseDescription': "Some elementary comp sci class",
            'courseDepartment': "CS"
        })
        # Checks to see if post method correctly adds courses to the database.
        self.assertEqual(Course.objects.filter(courseID=1).count(), 1,
                         msg="there should not be two same courses with identical courseNames in the "
                             "data base")
        self.assertEqual(len(Course.objects.all()), 2, "There should be a total of 2 courses in the database.")

        # checks to see if correct message is displayed when trying to add a course with the same ID.
        response = self.client.get('/courseAdd')
        self.assertIn(response.content, "Cannot add a course with the same courseName in the system",
                      msg="Response didn't correctly display the adding of"
                          "\"the same CourseName\"error message");

    def test_removeExistingCourse(self):
        """I'm assuming we do a post method on the button to remove the course from the database. I'll wait until
        it is implemented before writing this."""
        pass

    def test_removeNonExistingCourse(self):
        pass
