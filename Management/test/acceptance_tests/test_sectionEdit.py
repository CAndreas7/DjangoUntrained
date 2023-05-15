from django.test import TestCase, Client
from django.urls import reverse
from Management.models import Section, Course, User


class Test_EditSections(TestCase):

    def setUp(self):
        self.client = Client()
        self.TA1 = User.objects.create(email="SomeUser@user.com", password="testpassword", phone="", role=3)
        self.course1 = Course.objects.create(courseID=1, courseName="CS250",
                                             courseDescription="Some elementary comp sci class", courseDepartment="CS")
        self.section = Section.objects.create(courseID=self.course1, location="Here", startTime="7:00PM",endTime="7:50PM",
                                              capacity=100, TA=self.TA1, sectionID=2);

        self.editURL = reverse('sectionEdit', kwargs={'section_id': self.section.sectionID,
                                                      'course_id': self.section.courseID.courseID})

    def test_editLocation(self):
        response = self.client.post(self.editURL, {'location': "NotHere",
                                        'startTime': "7:00PM",
                                        'endTime': "7:50PM",
                                        'capacity': 100,
                                        'TA': self.TA1.email,
                                        'sectionID': 2,
        })

        self.assertEqual("NotHere", Section.objects.get(sectionID=self.section.sectionID).location,
                         "Unable to edit the location field in a session object via forms.")
        # no message field because it is a http response redirect object
        #self.assertEqual(response.context['message'], "Section was successfully edited!",
        #                 "message displayed was not correct")
    def test_editStartTime(self):
        self.client.post(self.editURL, {'location': "NotHere",
                                        'startTime': "10:00PM",
                                        'endTime': "7:50PM",
                                        'capacity': 100,
                                        'TA': self.TA1.email,
                                        'sectionID': 1,
                                        })

        self.assertEqual(Section.objects.get(sectionID=self.section.sectionID).startTime, "10:00PM",
                         "Unable to edit the startTime field in a session object via forms.")

        # no message field because it is a http response redirect object
        # self.assertEqual(response.context['message'], "Section was successfully edited!",
        #                 "message displayed was not correct")


    def test_editEndTime(self):
        self.client.post(self.editURL, {'location': "NotHere",
                                        'startTime': "7:00PM",
                                        'endTime': "10:50PM",
                                        'capacity': 100,
                                        'TA': self.TA1.email,
                                        'sectionID': 1,
                                        })

        self.assertEqual(Section.objects.get(sectionID=self.section.sectionID).endTime, "10:50PM",
                         "Unable to edit the endTime field in a session object via forms.")

        # no message field because it is a http response redirect object
        # self.assertEqual(response.context['message'], "Section was successfully edited!",
        #                 "message displayed was not correct")
    def test_editCapacity(self):
        response = self.client.post(self.editURL, {'location': "NotHere",
                                        'startTime': "7:00PM",
                                        'endTime': "10:50PM",
                                        'capacity': 200,
                                        'TA': self.TA1.email,
                                        'sectionID': 1,
                                        })

        self.assertEqual(Section.objects.get(sectionID=self.section.sectionID).capacity, 200,
                         "Unable to edit the capacity field in a session object via forms.")

        #no message field because it is a http response redirect object
        self.assertEqual(response.context['message'], "Section was successfully edited!",
                         "message displayed was not correct")
    def test_editTA(self):
        TA2 = User.objects.create(email="SomeUser2@user.com", password="testpassword", phone="", role=3)
        self.client.post(self.editURL, {'location': "NotHere",
                                        'startTime': "7:00PM",
                                        'endTime': "10:50PM",
                                        'capacity': 100,
                                        'TA': TA2.email,
                                        'sectionID': 1,
                                        })

        self.assertEqual(Section.objects.get(sectionID=self.section.sectionID).TA, TA2,
                         "Unable to edit the TA field in a session object via forms.")

        # no message field because it is a http response redirect object
        # self.assertEqual(response.context['message'], "Section was successfully edited!",
        #                 "message displayed was not correct")