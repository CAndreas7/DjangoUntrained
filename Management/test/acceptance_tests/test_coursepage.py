from django.test import TestCase, Client
from django.urls import reverse
from Management.models import Course


class Test_CoursesPage(TestCase):
    def setUp(self):
        self.client = Client()

        # creating a session?
        self.session = self.client.session
        self.session['roleSession'] = 1
        self.session.save()

        self.course1 = Course.objects.create(courseID=1, courseName="CS250",
                                            courseDescription="Some elementary comp sci class", courseDepartment="CS")
        self.course2 = Course.objects.create(courseID=2, courseName="CS350",
                                            courseDescription="Some class", courseDepartment="CS")

        #grabs all URLS for the page.
        self.coursesURL = reverse('courses')

        #This page doesn't exist?
        self.course1DeleteURL = reverse('courseDelete', kwargs={'course_id': self.course1.courseID})
        #these pages exists.
        self.sectionsOfCourse2URL = reverse('sections', kwargs={'course_id': self.course2.courseID})
        self.course1EditURL = reverse('courseEdit', kwargs={'course_id': self.course1.courseID})

        #for some reason, this page doesn't exist?
        self.course1UserURL = reverse('usersInCourse', kwargs={'course_id': self.course1.courseID})

    def test_display(self):
        response = self.client.get(self.coursesURL)

        queryset_courses = response.context['courses']
        list = []
        for x in queryset_courses:
            list.append(x)
        self.assertEqual(list[0].courseID, 1, "Course 1 is not being displayed")
        self.assertEqual(list[1].courseID, 2, "Course 2 is not being displayed")

    def test_display_instr(self):
        self.session['roleSession'] = 2;
        response = self.client.get(self.coursesURL)
        queryset_courses = response.context['courses']
        list = []
        for x in queryset_courses:
            list.append(x)
        self.assertEqual(list[0].courseID, 1, "Course 1 is not being displayed")
        self.assertEqual(list[1].courseID, 2, "Course 2 is not being displayed")

        self.assertNotEqual(list[0].courseID, 1, "Course 1 is being displayed")
        self.assertNotEqual(list[1].courseID, 2, "Course 2 is being displayed")

    def test_display_TA(self):
        self.session['roleSession'] = 3;
        response = self.client.get(self.coursesURL)
        queryset_courses = response.context['courses']
        list = []
        for x in queryset_courses:
            list.append(x)
        self.assertEqual(list[0].courseID, 1, "Course 1 is not being displayed")
        self.assertEqual(list[1].courseID, 2, "Course 2 is not being displayed")

        self.assertNotEqual(list[0].courseID, 1, "Course 1 is being displayed")
        self.assertNotEqual(list[1].courseID, 2, "Course 2 is being displayed")
    def test_RemoveCourse1(self):
        response = self.client.get(self.course1DeleteURL)

        self.assertEqual(response.status_code, 200, "status code was not 200")
        self.assertTemplateUsed(response, "main/Course/courses.html", "template was not correct template")
        self.assertEqual(Course.objects.filter(courseID=1).count(), 0, "course1 was not deleted from the database")


    def test_goToCourse2Sections(self):
        response = self.client.get(self.sectionsOfCourse2URL)

        self.assertEqual(response.status_code, 200, "response status code is not 200")
        self.assertTemplateUsed(response, 'main/Section/sections.html', "template was not correct template")

    def test_goToEditCourses1Page(self):
        response = self.client.get(self.course1EditURL)

        self.assertEqual(response.status_code, 200, "response status code is not 200")
        self.assertTemplateUsed(response, 'main/Course/courseEdit.html', "template was not correct template")

    def test_go_to_Course1_Users_page(self):
        response = self.client.get(self.course1UserURL)

        self.assertEqual(response.status_code, 200, "response status code is not 200")
        self.assertTemplateUsed(response, 'main/UserToCourse/courseUsers.html', "template was not correct template")