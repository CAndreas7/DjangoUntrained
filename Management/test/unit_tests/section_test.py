from django.test import TestCase
from Management.models import Section, Course
from Management.views import EditSections


class TestSection(TestCase):

    def test_add_section(self):
        # Create an instance of the EditSections class
        edit_sections = EditSections()

        # Call the addSection method to add a new section
        edit_sections.addSection(1, 'Test Location', '9:00AM', '10:00AM', 30, None, 1)

        # Check that a new section was added to the database
        self.assertEqual(Section.objects.count(), 1)

        # Check that the new section has the correct information
        section = Section.objects.first()
        self.assertEqual(section.sectionID, 1)
        self.assertEqual(section.location, 'Test Location')
        self.assertEqual(section.startTime, '9:00AM')
        self.assertEqual(section.endTime, '10:00AM')
        self.assertEqual(section.capacity, 30)
        self.assertIsNone(section.TA)
        self.assertEqual(section.courseID_id, 1)

    def test_view_section(self):

        Course.objects.create(courseName="test", courseID=1, courseDepartment="testdep", courseDescription='')
        Course.objects.create(courseName="test2", courseID=2, courseDepartment="testdep", courseDescription='')

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
        self.assertListEqual(list(sections), [Section.objects.get(sectionID=1), Section.objects.get(sectionID=2)])

    def test_remove_section(self):

        Course.objects.create(courseName="test", courseID=1, courseDepartment="testdep", courseDescription='')
        # Create some test data
        Section.objects.create(sectionID=1, location='Test Location 1', startTime='9:00AM', endTime='10:00AM',
                               capacity=30, TA=None, courseID_id=1)

        # Create an instance of the EditSections class
        edit_sections = EditSections()

        # Call the removeSection method to delete a section
        edit_sections.removeSection(1)

        # Check that the section was deleted from the database
        self.assertEqual(Section.objects.count(), 0)

    class SectionTest(TestCase):
        def test_get_id(self):

            Course.objects.create(courseName="test", courseID=1, courseDepartment="testdep", courseDescription='')

            # Create some test data
            section = Section.objects.create(sectionID=1, location='Test Location', startTime='9:00AM',
                                             endTime='10:00AM', capacity=30, TA=None, courseID_id=1)

            # Call the getID method to get the section ID
            section_id = section.getID()

            # Check that the method returns the correct section ID
            self.assertEqual(section_id, 1)

        def test_set_id(self):
            Course.objects.create(courseName="test", courseID=1, courseDepartment="testdep", courseDescription='')
            # Create some test data
            section = Section.objects.create(sectionID=1, location='Test Location', startTime='9:00AM',
                                             endTime='10:00AM', capacity=30, TA=None, courseID_id=1)

            # Call the setID method to update the section ID
            section.setID(2)

            # Check that the section ID was updated in the database
            section.refresh_from_db()
            self.assertEqual(section.sectionID, 2)
