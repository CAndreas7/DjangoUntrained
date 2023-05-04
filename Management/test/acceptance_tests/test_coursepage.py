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
        pass

    def test_removeExistingCourse(self):
        pass

    def test_removeNonExistingCourse(self):
        pass
    def test_goToSectionsPage(self):
        pass
    def test_goToEditCoursesPage(self):
        pass