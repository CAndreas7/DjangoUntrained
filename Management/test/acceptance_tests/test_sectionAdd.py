from django.test import TestCase, Client
from Management.models import Section,User,Course;

class Test_SectionAdd(TestCase):

    def setUp(self):

        self.client = Client()
        self.TA1 = User.objects.create(email="SomeUser@user.com", password="testpassword", phone="", role=3)

        self.course1 = Course.objects.create(courseID=1, courseName="CS250",
                                            courseDescription="Some elementary comp sci class", courseDepartment="CS")

        self.section = Section.objects.create(courseID=self.course1, location="Here", startTime="7:00PM", endTime="7:50PM",
                                              capacity=100, TA=self.TA1, sectionID=1);


    def test_addNewSection(self):
        self.client.post(('/sectionAdd/', {
            'courseID': 1,
            'location': 'United States',
            'startTime': '7:00AM',
            'endTime': '7:50AM',
            'capacity': 100,
            'TA': self.TA1,
            'sectionID': 2
        }))
        numSectionsID2 = Section.objects.filter(sectionID=2).count()
        #checks to see if the new section was added to the database.
        self.assertEqual(numSectionsID2, 1,
                         msg="the new section should have been added to the database ")
        self.assertEqual(len(Section.objects.all()), 2, "There should be a total of 2 sections in the database.")


    def test_addSameSection(self):
        self.client.post(('/sectionAdd/', {
            'courseID': 1,
            'location': 'Here',
            'startTime': '7:00PM',
            'endTime': '7:50PM',
            'capacity': 100,
            'TA': self.TA1,
            'sectionID': 1
        }))
        self.assertEqual(Section.objects.filter(sectionID=1).count(), 1,
                         msg="there should only be 1 section with this unique ID in the database ")
        self.assertEqual(len(Section.objects.all()), 1, "There should be a total of 1 section in the database.")

        #how would someone go about checking the display of the output

    def test_addSameID(self):
        self.client.post(('/sectionAdd/', {
            'courseID': 1,
            'location': 'United States',
            'startTime': '7:00AM',
            'endTime': '7:50AM',
            'capacity': 100,
            'TA': self.TA1,
            'sectionID': 1
        }))
        # checks to see if the new section was added to the database.
        self.assertEqual(Section.objects.filter(sectionID=2).count(), 1,
                         msg="the new section should have been added to the database ")
        self.assertEqual(len(Section.objects.all()), 2, "There should be a total of 2 sections in the database.")