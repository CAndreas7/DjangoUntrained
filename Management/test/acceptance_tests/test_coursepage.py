from django.test import TestCase, Client
from Management.models import Course


class Test_CoursesPage(TestCase):
    def setUp(self):
        self.client = Client()

        self.course = Course.objects.create(courseID="1", courseName="CS250",
                                            courseDescription="Some elementary comp sci class", courseDepartment="CS")
        self.course = Course.objects.create(courseID="2", courseName="CS350",
                                            courseDescription="Some class", courseDepartment="CS")
        self.course.save()


    def test_RemoveCourse(self):
        self.client.post('/courses', {
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

        """# checks to see if the website prints correct response contents.
        self.assertNotIn(response.content, 'Please fill out this field.', msg="Response displayed the adding"
                                                                      "\"the same course\"error message, when it "
                                                                      "shouldn't have");
        self.assertIn(response.content, 'course added successfully', msg="response did not show the correct message for"
                                                                         "adding a course successfully.")"""

    def test_removeExistingCourse(self):
        pass

    def test_removeNonExistingCourse(self):
        pass
    def test_goToSectionsPage(self):
        pass
    def test_goToEditCoursesPage(self):
        pass