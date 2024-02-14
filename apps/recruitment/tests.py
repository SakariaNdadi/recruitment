from django.test import TestCase
from django.contrib.auth.models import User
from .models import (
    Region,
    Town,
    Vacancy,
    Application,
    Interview,
    Bursary,
    BursaryApplication,
)
from apps.company.models import Position
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone


class RegionModelTestCase(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name="Test Region")

    def test_region_creation(self):
        self.assertEqual(self.region.name, "Test Region")


class TownModelTestCase(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name="Test Region")
        self.town = Town.objects.create(region=self.region, name="Test Town")

    def test_town_creation(self):
        self.assertEqual(self.town.region, self.region)
        self.assertEqual(self.town.name, "Test Town")


class VacancyModelTestCase(TestCase):
    def setUp(self):
        self.position = Position.objects.create(title="Test Position")
        self.region = Region.objects.create(name="Test Region")
        self.town = Town.objects.create(region=self.region, name="Test Town")
        self.vacancy = Vacancy.objects.create(
            position=self.position,
            town=self.town,
            deadline=timezone.now() + timedelta(days=1),
            is_published=True,
            is_external=False,
            remarks="Test Remarks",
        )

    def test_vacancy_creation(self):
        self.assertEqual(self.vacancy.position, self.position)
        self.assertEqual(self.vacancy.town, self.town)
        self.assertTrue(self.vacancy.is_published)
        self.assertFalse(self.vacancy.is_external)
        self.assertEqual(self.vacancy.remarks, "Test Remarks")


class ApplicationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.position = Position.objects.create(title="Test Position")
        self.region = Region.objects.create(name="Test Region")
        self.town = Town.objects.create(region=self.region, name="Test Town")
        self.vacancy = Vacancy.objects.create(
            position=self.position,
            town=self.town,
            deadline=timezone.now() + timedelta(days=1),
            is_published=True,
            is_external=False,
            remarks="Test Remarks",
        )
        self.application = Application.objects.create(
            user=self.user,
            vacancy=self.vacancy,
            status=Application.Status.SUBMITTED,
            cover_letter="Test Cover Letter",
            remarks="Test Remarks",
            document=None,
        )

    def test_application_creation(self):
        self.assertEqual(self.application.user, self.user)
        self.assertEqual(self.application.vacancy, self.vacancy)
        self.assertEqual(self.application.status, Application.Status.SUBMITTED)
        self.assertEqual(self.application.cover_letter, "Test Cover Letter")
        self.assertEqual(self.application.remarks, "Test Remarks")
        self.assertIsNone(self.application.document)


class InterviewModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.position = Position.objects.create(title="Test Position")
        self.region = Region.objects.create(name="Test Region")
        self.town = Town.objects.create(region=self.region, name="Test Town")
        self.vacancy = Vacancy.objects.create(
            position=self.position,
            town=self.town,
            deadline=timezone.now() + timedelta(days=1),
            is_published=True,
            is_external=False,
            remarks="Test Remarks",
        )
        self.application = Application.objects.create(
            user=self.user,
            vacancy=self.vacancy,
            status=Application.Status.SUBMITTED,
            cover_letter="Test Cover Letter",
            remarks="Test Remarks",
            document=None,
        )
        self.interview = Interview.objects.create(
            application=self.application,
            dateTime=timezone.now() + timedelta(days=1),
            status=Interview.Status.SET,
            description="Test Description",
            location=Interview.Location.ONLINE,
            interview_type=Interview.InterviewType.IN_PERSON,
            duration=30,
            reschedule_reason="Test Reschedule Reason",
            reschedule_date=None,
            rejection_reasons="",
        )

    def test_interview_creation(self):
        self.assertEqual(self.interview.application, self.application)
        self.assertEqual(self.interview.status, Interview.Status.SET)
        self.assertEqual(self.interview.description, "Test Description")
        self.assertEqual(self.interview.location, Interview.Location.ONLINE)
        self.assertEqual(
            self.interview.interview_type, Interview.InterviewType.IN_PERSON
        )
        self.assertEqual(self.interview.duration, 30)
        self.assertEqual(self.interview.reschedule_reason, "Test Reschedule Reason")
        self.assertIsNone(self.interview.reschedule_date)
        self.assertEqual(self.interview.rejection_reasons, "")


class BursaryModelTestCase(TestCase):
    def setUp(self):
        self.bursary = Bursary.objects.create(
            title="Test Bursary",
            criteria="Test Criteria",
            is_external=False,
            deadline=timezone.now() + timedelta(days=1),
            is_published=True,
        )

    def test_bursary_creation(self):
        self.assertEqual(self.bursary.title, "Test Bursary")
        self.assertEqual(self.bursary.criteria, "Test Criteria")
        self.assertFalse(self.bursary.is_external)
        self.assertTrue(self.bursary.is_published)


class BursaryApplicationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.bursary = Bursary.objects.create(
            title="Test Bursary",
            criteria="Test Criteria",
            is_external=False,
            deadline=timezone.now() + timedelta(days=1),
            is_published=True,
        )
        self.bursary_application = BursaryApplication.objects.create(
            bursary=self.bursary,
            applicant=self.user,
            status=BursaryApplication.STATUS_TYPE.SUBMITTED,
            field_of_study="Test Field of Study",
            relevancy_to_current_occupation="Test Relevancy to Current Occupation",
            institute="Test Institute",
            mode_of_study=BursaryApplication.MODE_OF_STUDY.FULL_TIME,
            mode_of_study_reason="Test Mode of Study Reason",
            minimum_study_duration=1,
            maximum_study_duration=4,
            commencement_date=datetime.now().date(),
            tuition_fees=1000,
            travel_fees=500,
            accommodation_fees=800,
            books_fees=300,
            other_fees=200,
            other_fees_specification="Test Other Fees Specification",
            first_year_total_fees=2800,
            gross_total_all_years=3000,
        )

    def test_bursary_application_creation(self):
        self.assertEqual(self.bursary_application.bursary, self.bursary)
        self.assertEqual(self.bursary_application.applicant, self.user)
        self.assertEqual(
            self.bursary_application.status, BursaryApplication.STATUS_TYPE.SUBMITTED
        )
        self.assertEqual(self.bursary_application.field_of_study, "Test Field of Study")
        self.assertEqual(
            self.bursary_application.relevancy_to_current_occupation,
            "Test Relevancy to Current Occupation",
        )
        self.assertEqual(self.bursary_application.institute, "Test Institute")
        self.assertEqual(
            self.bursary_application.mode_of_study,
            BursaryApplication.MODE_OF_STUDY.FULL_TIME,
        )
        self.assertEqual(
            self.bursary_application.mode_of_study_reason, "Test Mode of Study Reason"
        )
        self.assertEqual(self.bursary_application.minimum_study_duration, 1)
        self.assertEqual(self.bursary_application.maximum_study_duration, 4)
        self.assertEqual(
            self.bursary_application.commencement_date, datetime.now().date()
        )
        self.assertEqual(self.bursary_application.tuition_fees, 1000)
        self.assertEqual(self.bursary_application.travel_fees, 500)
        self.assertEqual(self.bursary_application.accommodation_fees, 800)
        self.assertEqual(self.bursary_application.books_fees, 300)
        self.assertEqual(self.bursary_application.other_fees, 200)
        self.assertEqual(
            self.bursary_application.other_fees_specification,
            "Test Other Fees Specification",
        )
        self.assertEqual(self.bursary_application.first_year_total_fees, 2800)
        self.assertEqual(self.bursary_application.gross_total_all_years, 3000)
