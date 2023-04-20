from django.test import TestCase
from Management.models import Section, Course
from Management.views import EditSections


# EditSections.addSection()
#
# Precondition: No section exists with the given information/primary key.
# Postcondition: A new section will be added to the database with given parameters.
# Side Effects: A new entry will be added to the database/models
# SectionID(IN): Unique identifier for each section, the section number.
# Name(IN): Name/title of the course.
# Department(IN): The department the course is in.

# EditSections.viewSection()
#
# Precondition:  There exists at least one section in the database
# Postcondition:  A table in a HTML page is created and filled with information about the sections
# Side effects:  This is a read operation and the table is destroyed when we leave the page/re render
# No input, the method will read everything from the model/database

# EditSections.removeSection(SectionID)
# Precondition:  The database has at least 1 section in it, and the user has permission to remove sections
# Postcondition:  The record associated with the given SectionID is deleted from database
# Side Effects:  Sections shouldn’t have many other connections that rely on a section existing, so no side effects
# SectionID(IN):  The given sectionID to identify the record to delete

# Sections.getID()
#
# Precondition:  The section has an ID entered in the database
# Postcondition:  The method returns the section’s sectionID
# Side effects:  None
# No inputs

# Section.setID(sectionID)
#
# Precondition:  The section should have an id, but the method will work without it
# Postcondition:  The given section will have its sectionID updated
# Side effects:  Anywhere that this sectionID was displayed will be changed to reflect this change
# SectionID(IN):  This parameter is the new sectionID that will be entered in the database




class TestSection(TestCase):

    def setup(self):

        Course.objects.create(courseName="test", courseID=1, courseDepartment="testdep", courseDescription='')

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
