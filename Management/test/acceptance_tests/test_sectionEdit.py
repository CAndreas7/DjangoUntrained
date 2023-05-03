from django.test import TestCase, Client
from Management.models import Section, User


class Test_EditSections(TestCase):

    def setUp(self):
        self.client = Client()
        self.section = Section.objects.create(courseID="1", location="Here", startTime="7:00PM",endTime="7:50PM",
                                              capacity=100, TA="TAobject",sectionID=1);

    # these are heavily dependent on whether you clicked on the course so it prompts you to a
    # edit course name, changing it's id
    def test_editLocation(self):
        self.client.post(location="NotHere")

        self.assertEqual(Section.objects.get(sectionID=1).location, "NotHere",
                         "Unable to edit the location field in a session object via forms.")

    def test_editStartTime(self):
        self.client.post(startTime="10:00PM")

        self.assertEqual(Section.objects.get(sectionID=1).startTime, "10:00PM",
                         "Unable to edit the startTime field in a session object via forms.")


    def test_editEndTime(self):
        self.client.post(endTime="10:50PM")

        self.assertEqual(Section.objects.get(sectionID=1).endTime, "10:50PM",
                         "Unable to edit the endTime field in a session object via forms.")
    def test_editCapacity(self):
        self.client.post(capacity=200)

        self.assertEqual(Section.objects.get(sectionID=1).capacity, 200,
                         "Unable to edit the capacity field in a session object via forms.")
    def test_editTA(self):
        self.client.post(TA="NotTA")

        self.assertEqual(Section.objects.get(sectionID=1).TA, "NotTA",
                         "Unable to edit the TA field in a session object via forms.")
    def test_editSectionID(self):
        self.client.post(sectionID=2)

        self.assertEqual(Section.objects.get(sectionID=2).count(), 1, "There is either 0 or more than 1 sections with"
                                                                      "this sectionID.")
        self.assertEqual(Section.objects.get(sectionID=2).sectionID, 2,
                         "Unable to edit the sectionID field in a session object via forms.")