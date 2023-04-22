from unittest.mock import patch, MagicMock
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from Management.models import Section, Course
from Management.views import EditSections
from django.test import RequestFactory


class TestSection(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.course = Course.objects.create(courseName="test", courseID=1, courseDepartment="testdep",
                                            courseDescription='')
        self.edit_sections = EditSections()

    def test_view_section(self):
        try:
            # Try to get a Course object with the given courseID
            course = Course.objects.get(courseID=1)
        except ObjectDoesNotExist:
            # If no Course object with the given courseID exists, create a new one
            course = Course.objects.create(courseName="test", courseID=1, courseDepartment="testdep",
                                           courseDescription='')

        try:
            # Try to get a Course object with the given courseID
            course = Course.objects.get(courseID=2)
        except ObjectDoesNotExist:
            # If no Course object with the given courseID exists, create a new one
            course = Course.objects.create(courseName="test2", courseID=2, courseDepartment="testdep",
                                           courseDescription='')

        # Create some test data
        Section.objects.create(sectionID=1, location='Test Location 1', startTime='9:00AM', endTime='10:00AM',
                               capacity=30, TA=None, courseID_id=1)
        Section.objects.create(sectionID=2, location='Test Location 2', startTime='10:00AM', endTime='11:00AM',
                               capacity=40, TA=None, courseID_id=2)

        # Create an instance of the EditSections class
        edit_sections = EditSections()

        # Call the viewSection method to get a list of all sections
        sections = edit_sections.viewSection()

        # Check that the list contains all sections in the database
        self.assertListEqual(list(sections), [Section.objects.get(sectionID=1), Section.objects.get(sectionID=2)],
                             msg="List should contain all sections in the database")

    def test_remove_section(self):

        def test_remove_section(self):
            try:
                # Try to get a Course object with the given courseID
                course = Course.objects.get(courseID=1)
            except ObjectDoesNotExist:
                # If no Course object with the given courseID exists, create a new one
                course = Course.objects.create(courseName="test", courseID=1, courseDepartment="testdep",
                                               courseDescription='')

            # Create some test data
            Section.objects.create(sectionID=1, location='Test Location 1', startTime='9:00AM', endTime='10:00AM',
                                   capacity=30, TA=None, courseID_id=1)

            # Create an instance of the EditSections class
            edit_sections = EditSections()

            # Call the removeSection method to delete a section
            edit_sections.removeSection(1)

            # Check that the section was deleted from the database
            self.assertEqual(Section.objects.count(), 0, msg="section isn't deleted from DB")

    def test_get_id(self):
        try:
            # Try to get a Course object with the given courseID
            course = Course.objects.get(courseID=1)
        except ObjectDoesNotExist:
            # If no Course object with the given courseID exists, create a new one
            course = Course.objects.create(courseName="test", courseID=1, courseDepartment="testdep",
                                           courseDescription='')

        # Create some test data
        section = Section.objects.create(sectionID=1, location='Test Location', startTime='9:00AM',
                                         endTime='10:00AM', capacity=30, TA=None, courseID_id=1)

        # Call the getID method to get the section ID
        section_id = section.getID()

        # Check that the method returns the correct section ID
        self.assertEqual(section_id, 1, msg="did not return correct section id")

    def test_set_id(self):
        try:
            # Try to get a Course object with the given courseID
            course = Course.objects.get(courseID=1)
        except ObjectDoesNotExist:
            # If no Course object with the given courseID exists, create a new one
            course = Course.objects.create(courseName="test", courseID=1, courseDepartment="testdep",
                                           courseDescription='')

        # Create some test data
        section = Section.objects.create(sectionID=1, location='Test Location', startTime='9:00AM',
                                         endTime='10:00AM', capacity=30, TA=None, courseID_id=1)

        # Call the setID method to update the section ID
        section.setID(2)

        # Check that the section ID was updated in the database
        section.refresh_from_db()
        self.assertEqual(section.sectionID, 2, msg="section id was no updated")

    class AddSectionTestCase(TestCase):
        @patch('main.views.SectionForm')
        @patch('main.views.Section')
        def test_post_request_with_valid_form_data(self, mock_section, mock_section_form):
            # Set up mock form
            mock_form = mock_section_form.return_value
            mock_form.is_valid.return_value = True
            form_data = {
                'courseID': 'CS101',
                'location': 'Room 101',
                'startTime': '09:00',
                'endTime': '10:00',
                'capacity': 30,
                'TA': 'John Doe',
                'sectionID': 'A'
            }
            mock_form.cleaned_data = form_data

            # Set up mock request
            mock_request = MagicMock()
            mock_request.method = 'POST'
            mock_request.POST = form_data

            # Call the addSection method
            response = EditSections.addSection(mock_request)

            # Check that a new Section object was created with the correct data
            mock_section.assert_called_once_with(**form_data)

            # Check that the new section was saved to the database
            new_section = mock_section.return_value
            new_section.save.assert_called_once()

            # Check that the response is an HttpResponse with the text 'Section added successfully'
            self.assertContains(response, 'Section added successfully')
