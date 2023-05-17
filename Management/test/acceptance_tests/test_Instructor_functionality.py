from django.test import TestCase, Client
from django.urls import reverse
from Management.models import User, Course, Section

class Test_Instructor_Functionality(TestCase):
    def setUp(self):
        self.client = Client()
        self.session = self.client.session
        self.session['roleSession'] = 2
        self.session.save()

        self.Instructor1 = User.objects.create(email="SomeUser3@user.com",
                                               password="testpassword",
                                               phone="",
                                               role=2)
        self.Instructor2 = User.objects.create(email="SomeUser4@user.com",
                                               password="testpassword",
                                               phone="",
                                               role=2)
        self.course1 = Course.objects.create(courseID=1, courseName="CS250",
                                             courseDescription="Some elementary comp sci class", courseDepartment="CS")
        self.course2 = Course.objects.create(courseID=2, courseName="CS350",
                                             courseDescription="Some class", courseDepartment="CS")

        self.TA1 = User.objects.create(email="SomeUser@user.com", password="testpassword", phone="", role=3)

        self.section = Section.objects.create(courseID=self.course2, location="Here", startTime="7:00PM",
                                              endTime="7:50PM",
                                              capacity=100, TA=self.TA1, sectionID=2);

        # all button urls that exist on the page once initializing above objects.
        self.sectionsOfCourse2URL = reverse('sections', kwargs={'course_id': self.course2.courseID})
        self.sectionAddURL = reverse('sectionAdd', kwargs={'course_id': self.course2.courseID})
        self.sectionEditURL = reverse('sectionEdit', kwargs={'course_id': self.course2.courseID,
                                                             'section_id': self.section.sectionID})
        self.sectionDeleteURL = reverse('sectionDelete', kwargs={'course_id': self.course2.courseID,
                                                                 'section_id': self.section.sectionID})

        self.userAddURL = reverse('userAdd')
        self.accountInfoURL = reverse('users')
        self.Instructor1EditURL = reverse('userEdit', kwargs={'email_id': self.Instructor1.email})
        self.Instructor2EditURL = reverse('userEdit', kwargs={'email_id': self.Instructor2.email})
        self.accountInfoURL = reverse('users')
        self.sectionAddURL = reverse('sectionAdd', kwargs={'course_id': self.course1.courseID})

        # grabs all URLS for the page.
        self.coursesURL = reverse('courses')

    def test_instructor_login(self):
        response = self.client.post('/', {
            'email': 'SomeUser3@user.edu',
            'password': 'testpassword'},
                                    follow=True)
        self.assertTemplateUsed(response, 'main/home.html')
    def test_instructor_edit_contact_info(self):
        self.client.post(self.Instructor1EditURL, {
            'email': "newEmail@user.com",
            'password': "testpassword",
            'fName': "Me",
            'lName': "not me",
            'phone': 43,
            'role': 3,
        })

        self.assertEqual(User.objects.filter(email="newEmail@user.com").count(), 1,
                         "There are more than 1 user object with this unique ID")
        self.assertEqual(User.objects.filter(email="SomeUser1@user.com").count(), 0,
                         "The previous unique email ID still exists.")
        self.assertEqual(len(User.objects.all()), 3, "There should be a total of 3 User in the database.")


    def test_instructor_view_course_assignments(self):
        response = self.client.get(self.coursesURL)
        queryset_courses = response.context['courses']
        list = []
        for x in queryset_courses:
            list.append(x)
        self.assertEqual(list[0].courseID, 1, "Course 1 is not being displayed")
        self.assertEqual(list[1].courseID, 2, "Course 2 is not being displayed")

    def test_instructor_view_TA_assignments(self):
        response = self.client.get(self.sectionsOfCourse2URL)

        queryset_sections = response.context['sections']
        list = []
        for section in queryset_sections:
            list.append(section)
        self.assertEqual(list[0].sectionID, 2, "Course 1 is not being displayed")

    def test_instructor_assign_TA_to_lab_section(self):
        response = self.client.post(self.sectionAddURL, {
            'sectionID': 3,
            'location': 'MS200',
            'startTime': '7:00AM',
            'endTime': '7:50AM',
            'capacity': 100,
            'TA': self.TA1.email,
            'courseID': self.course1
        })
        # checks to see if the response didn't blow up.
        # self.assertEqual(response.status_code, 200, "Status code is not 200")
        # checks to see if the new section was added to the database.
        self.assertEqual(Section.objects.filter(sectionID=2).count(), 1,
                         msg="the new section should have been added to the database ")
        self.assertEqual(len(Section.objects.all()), 2, "There should be a total of 1 sections in the database.")

        self.assertEqual(response.context['message'], "Section successfully added.",
                         "message displayed was not correct")

    def test_instructor_read_contact_info(self):
        response = self.client.get(self.accountInfoURL)

        queryset_users = response.context['results']
        list = []
        for user in queryset_users:
            list.append(user)
        self.assertEqual(list[0].email, "SomeUser3@user.com", "Course 1 is not being displayed")
        self.assertEqual(list[1].email, "SomeUser4@user.com", "Course 2 is not being displayed")
        self.assertEqual(list[2].email, "SomeUser@user.com", "Course 2 is not being displayed")
