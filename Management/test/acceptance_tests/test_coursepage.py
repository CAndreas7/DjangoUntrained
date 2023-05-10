from django.test import TestCase, Client
from django.urls import reverse
from Management.models import Course


class Test_CoursesPage(TestCase):
    def setUp(self):
        self.client = Client()

        self.course1 = Course.objects.create(courseID=1, courseName="CS250",
                                            courseDescription="Some elementary comp sci class", courseDepartment="CS")
        self.course2 = Course.objects.create(courseID=2, courseName="CS350",
                                            courseDescription="Some class", courseDepartment="CS")

        #grabs all URLS for the page.
        self.coursesURL = reverse('courses')
        self.course1DeleteURL = reverse('courseDelete', kwargs={'course_id': self.course1.courseID})
        self.sectionsOfCourse2URL = reverse('sections', kwargs={'course_id': self.course2.courseID})
        self.course1EditURL = reverse('courseEdit', kwargs={'course_id': self.course1.courseID})
        self.course1UserURL = reverse('usersInCourse', kwargs={'course_id': self.course1.courseID})

    def test_RemoveCourse1(self):
        self.client.get(self.course1DeleteURL)

        self.assertEqual(Course.objects.filter(courseID=1).count(), 0, "course1 was not deleted from the database")


    def test_goToCourse2Sections(self):
        response = self.client.get(self.sectionsOfCourse2URL)

        self.assertEqual(response.status_code, 200, "response status code is not 200")
    def test_goToEditCourses1Page(self):
        response = self.client.get(self.course1EditURL)

        self.assertEqual(response.status_code, 200, "response status code is not 200")

    def test_go_to_Course1_Users_page(self):
        response = self.client.get(self.course1UserURL)

        self.assertEqual(response.status_code, 200, "response status code is not 200")