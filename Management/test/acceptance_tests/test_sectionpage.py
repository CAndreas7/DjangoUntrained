from django.test import TestCase, Client
from django.urls import reverse
from Management.models import Section,Course,User


class Test_SectionPage(TestCase):
    def setUp(self):
        self.client = Client()
        self.TA1 = User.objects.create(email="SomeUser@user.com", password="testpassword", phone="", role=3)
        self.course2 = Course.objects.create(courseID="2", courseName="CS350",
                                             courseDescription="Some class", courseDepartment="CS")
        self.section = Section.objects.create(courseID=self.course2, location="Here", startTime="7:00PM",
                                              endTime="7:50PM",
                                              capacity=100, TA=self.TA1, sectionID=2);

        #all button urls that exist on the page once initializing above objects.
        self.sectionsOfCourse2URL = reverse('sections', kwargs={'course_id': self.course2.courseID})
        self.sectionAddURL = reverse('sectionAdd', kwargs={'course_id': self.course2.courseID})
        self.sectionEditURL = reverse('sectionEdit', kwargs={'course_id': self.course2.courseID,
                                                             'section_id': self.section.sectionID})
        self.sectionDeleteURL = reverse('sectionDelete', kwargs={'course_id': self.course2.courseID,
                                                                'section_id': self.section.sectionID})

    def test_goToEditSection(self):
        response = self.client.get(self.sectionEditURL)

        self.assertEqual(response.status_code, 200, "status code is not 200.")
        self.assertTemplateUsed(response, 'main/Section/sectionEdit.html')
    def test_deleteSection(self):
        response = self.client.get(self.sectionDeleteURL)

        self.assertEqual(Section.objects.filter(sectionID=2).count(), 0, "Section was not properly deleted")
        self.assertRedirects(response, 'main/Section/sections.html')

    def test_goToAddSection(self):
        response = self.client.get(self.sectionAddURL)

        self.assertEqual(response.status_code, 200, "status code is not 200.")
        self.assertTemplateUsed(response, 'main/Section/addSection.html')
