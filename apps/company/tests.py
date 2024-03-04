from django.test import TestCase
from django.contrib.auth.models import User
from .models import Department, Division, Qualification, Position


class DepartmentModelTestCase(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name="Test Department",
            description="Test Department Description",
            chief=None,
        )

    def test_department_creation(self):
        self.assertEqual(self.department.name, "Test Department")
        self.assertEqual(self.department.description, "Test Department Description")
        self.assertIsNone(self.department.chief)


class DivisionModelTestCase(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name="Test Department",
            description="Test Department Description",
            chief=None,
        )
        self.division = Division.objects.create(
            title="Test Division",
            description="Test Division Description",
            department=self.department,
            manager=None,
        )

    def test_division_creation(self):
        self.assertEqual(self.division.title, "Test Division")
        self.assertEqual(self.division.description, "Test Division Description")
        self.assertEqual(self.division.department, self.department)
        self.assertIsNone(self.division.manager)


class QualificationModelTestCase(TestCase):
    def setUp(self):
        self.qualification = Qualification.objects.create(
            type=Qualification.Type.BACHELORS, title="Test Qualification"
        )

    def test_qualification_creation(self):
        self.assertEqual(self.qualification.type, Qualification.Type.BACHELORS)
        self.assertEqual(self.qualification.title, "Test Qualification")


class PositionModelTestCase(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name="Test Department",
            description="Test Department Description",
            chief=None,
        )
        self.division = Division.objects.create(
            title="Test Division",
            description="Test Division Description",
            department=self.department,
            manager=None,
        )
        self.position = Position.objects.create(
            title="Test Position",
            key_purpose="Test Key Purpose",
            key_result_areas="Test Key Result Areas",
            key_knowledge="Test Key Knowledge",
            personality_requirements="Test Personality Requirements",
            experience="Test Experience",
            job_grade=Position.JobGrade.A1,
            division=self.division,
            line_manager=None,
        )

    def test_position_creation(self):
        self.assertEqual(self.position.title, "Test Position")
        self.assertEqual(self.position.key_purpose, "Test Key Purpose")
        self.assertEqual(self.position.key_result_areas, "Test Key Result Areas")
        self.assertEqual(self.position.key_knowledge, "Test Key Knowledge")
        self.assertEqual(
            self.position.personality_requirements, "Test Personality Requirements"
        )
        self.assertEqual(self.position.experience, "Test Experience")
        self.assertEqual(self.position.job_grade, Position.JobGrade.A1)
        self.assertEqual(self.position.division, self.division)
        self.assertIsNone(self.position.line_manager)
