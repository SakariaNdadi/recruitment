from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Experience, Education, Certification
from apps.company.models import Position, Qualification
from datetime import date


class ProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="test@example.com", password="testpassword"
        )
        self.position = Position.objects.create(title="Test Position")
        self.profile = Profile.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            user_type=Profile.UserType.APPLICANT,
            nationality="us",
            population_group=Profile.PopulationGroup.RACIALLY_ADVANTAGED,
            id_number=12345678901,
            gender=Profile.Gender.MALE,
            date_of_birth=date(1990, 5, 15),
            primary_contact="+1234567890",
            position=self.position,
            employee_id=12345,
            call_center_number=987654321,
            appointed_date=date(2022, 1, 1),
            postal_address="123 Test St, Test City, Test Country",
            linkedin="https://www.linkedin.com/testuser",
            picture=None,
            cv=None,
            is_created=False,
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.first_name, "John")
        self.assertEqual(self.profile.last_name, "Doe")
        self.assertEqual(self.profile.user_type, Profile.UserType.APPLICANT)
        self.assertEqual(self.profile.nationality, "us")
        self.assertEqual(
            self.profile.population_group, Profile.PopulationGroup.RACIALLY_ADVANTAGED
        )
        self.assertEqual(self.profile.id_number, 12345678901)
        self.assertEqual(self.profile.gender, Profile.Gender.MALE)
        self.assertEqual(self.profile.date_of_birth, date(1990, 5, 15))
        self.assertEqual(str(self.profile.primary_contact), "+1234567890")
        self.assertEqual(self.profile.position, self.position)
        self.assertEqual(self.profile.employee_id, 12345)
        self.assertEqual(self.profile.call_center_number, 987654321)
        self.assertEqual(self.profile.appointed_date, date(2022, 1, 1))
        self.assertEqual(
            self.profile.postal_address, "123 Test St, Test City, Test Country"
        )
        self.assertEqual(self.profile.linkedin, "https://www.linkedin.com/testuser")
        self.assertIsNone(self.profile.picture)
        self.assertIsNone(self.profile.cv)
        self.assertFalse(self.profile.is_created)


class ExperienceModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="test@example.com", password="testpassword"
        )
        self.experience = Experience.objects.create(
            user=self.user,
            job_title="Test Job",
            job_description="Test job description",
            company_name="Test Company",
            employment_type="Full-time",
            location="Test Location",
            employment_status=True,
            industry="Test Industry",
            start_date=date(2020, 1, 1),
            end_date=date(2021, 1, 1),
        )

    def test_experience_creation(self):
        self.assertEqual(self.experience.job_title, "Test Job")
        self.assertEqual(self.experience.job_description, "Test job description")
        self.assertEqual(self.experience.company_name, "Test Company")
        self.assertEqual(self.experience.employment_type, "Full-time")
        self.assertEqual(self.experience.location, "Test Location")
        self.assertTrue(self.experience.employment_status)
        self.assertEqual(self.experience.industry, "Test Industry")
        self.assertEqual(self.experience.start_date, date(2020, 1, 1))
        self.assertEqual(self.experience.end_date, date(2021, 1, 1))


class EducationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="test@example.com", password="testpassword"
        )
        self.qualification = Qualification.objects.create(title="Test Qualification")
        self.education = Education.objects.create(
            user=self.user,
            institution_name="Test Institution",
            qualification=self.qualification,
            obtained_date=date(2019, 1, 1),
            file=None,
        )

    def test_education_creation(self):
        self.assertEqual(self.education.institution_name, "Test Institution")
        self.assertEqual(self.education.qualification, self.qualification)
        self.assertEqual(self.education.obtained_date, date(2019, 1, 1))
        self.assertIsNone(self.education.file)


class CertificationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="test@example.com", password="testpassword"
        )
        self.certification = Certification.objects.create(
            user=self.user,
            title="Test Certification",
            institution_name="Test Institution",
            obtained_date=date(2020, 1, 1),
            validity=2,
            file=None,
        )

    def test_certification_creation(self):
        self.assertEqual(self.certification.title, "Test Certification")
        self.assertEqual(self.certification.institution_name, "Test Institution")
        self.assertEqual(self.certification.obtained_date, date(2020, 1, 1))
        self.assertEqual(self.certification.validity, 2)
        self.assertIsNone(self.certification.file)
