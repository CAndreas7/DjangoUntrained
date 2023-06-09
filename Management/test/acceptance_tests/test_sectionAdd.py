from django.test import TestCase, Client
from django.urls import reverse
from Management.models import Section,User,Course;

class Test_SectionAdd(TestCase):
        #theses don't run because kevin didn't change redirect to render.
    def setUp(self):

        self.client = Client()

        # creating a session?
        self.session = self.client.session
        self.session['roleSession'] = 1
        self.session.save()

        self.TA1 = User.objects.create(email="SomeUser@user.com", password="testpassword", phone="", role=3)

        self.course1 = Course.objects.create(courseID=1, courseName="CS250",
                                            courseDescription="Some elementary comp sci class", courseDepartment="CS")

        self.section = Section.objects.create(courseID=self.course1, location="Here", startTime="7:00PM", endTime="7:50PM",
                                              capacity=100, TA=self.TA1, sectionID=1);


        self.sectionAddURL = reverse('sectionAdd', kwargs={'course_id': self.course1.courseID})


    def test_addNewSection(self):
        response = self.client.post(self.sectionAddURL, {
            'sectionID': 2,
            'location': 'MS200',
            'startTime': '7:00AM',
            'endTime': '7:50AM',
            'capacity': 100,
            'TA': self.TA1.email,
        })


        self.assertEqual(Section.objects.filter(sectionID=2).count(), 1,
                         msg="the new section should have been added to the database ")
        self.assertEqual(len(Section.objects.all()), 2, "There should be a total of 2 sections in the database.")

        self.assertEqual(response.context['message'], "Section successfully added.", "message displayed was not correct")

    def test_instructor_add(self):
        self.session['roleSession'] = 2
        self.client.post(self.sectionAddURL, {
            'sectionID': 2,
            'location': 'MS200',
            'startTime': '7:00AM',
            'endTime': '7:50AM',
            'capacity': 100,
            'TA': self.TA1.email,
        })

        self.assertNotEqual(Section.objects.filter(sectionID=2).count(), 1,
                         msg="instructors cannot create a new section.")

    def test_TA_add(self):
        self.session['roleSession'] = 3
        self.client.post(self.sectionAddURL, {
                'sectionID': 2,
                'location': 'MS200',
                'startTime': '7:00AM',
                'endTime': '7:50AM',
                'capacity': 100,
                'TA': self.TA1.email,
            })

        self.assertNotEqual(Section.objects.filter(sectionID=2).count(), 1,
                                msg="instructors cannot create a new section.")



    def test_addSameSection(self):
        self.client.post(self.sectionAddURL, {
            'sectionID': 2,
            'location': 'MS200',
            'startTime': '7:00AM',
            'endTime': '7:50AM',
            'capacity': 100,
            'TA': self.TA1.email,
        })

        response = self.client.post(self.sectionAddURL, {
            'location': 'MS200',
            'startTime': '7:030PM',
            'endTime': '7:503PM',
            'capacity': 1020,
            'TA': self.TA1.email,
            'sectionID': 2
        })


        self.assertEqual(Section.objects.filter(sectionID=1).count(), 1,
                         msg="there should only be 1 section with this unique ID in the database ")
        self.assertEqual(len(Section.objects.all()), 2, "There should be a total of 2 section in the database.")

        self.assertEqual(response.context['message'], "Section ID is either already used or Invalid Form Data",
                         "message displayed was not correct")



    def test_addSameID(self):
        self.client.post(self.sectionAddURL, {
            'sectionID': 2,
            'location': 'MS200',
            'startTime': '7:00AM',
            'endTime': '7:50AM',
            'capacity': 100,
            'TA': self.TA1.email,
        })

        response = self.client.post(self.sectionAddURL, {
            'location': 'Here',
            'startTime': '7:00PM',
            'endTime': '7:50PM',
            'capacity': 100,
            'TA': self.TA1.email,
            'sectionID': 2
        })

        self.assertEqual(Section.objects.filter(sectionID=1).count(), 1,
                         msg="there should only be 1 section with this unique ID in the database ")
        self.assertEqual(len(Section.objects.all()), 2, "There should be a total of 2 section in the database.")

        self.assertEqual(response.context['message'], "Section ID is either already used or Invalid Form Data",
                         "message displayed was not correct")

