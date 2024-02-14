from rest_framework.serializers import ModelSerializer
from apps.accounts.models import Profile, Education, Experience, Certification
from apps.recruitment.models import Application, Vacancy, Interview


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "user",
            "first_name",
            "last_name",
            "user_type",
            "primary_contact",
            "secondary_contact",
            "id_number",
            "gender",
            "population_group",
            "date_of_birth",
            "position",
            "employee_id",
            "division",
            "call_center_number",
            "picture",
            "linkedin",
            "cv",
        )


class EducationSerializer(ModelSerializer):
    class Meta:
        model = Education
        fields = (
            "user",
            "institution_name",
            "qualification",
            "obtained_date",
            "file",
        )


class ExperienceSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = (
            "user",
            "job_title",
            "job_description",
            "company_name",
            "employment_type",
            "location",
            "employment_status",
            "industry",
            "start_date",
            "end_date",
        )


class CertificationSerializer(ModelSerializer):
    class Meta:
        model = Certification
        fields = (
            "user",
            "title",
            "institution_name",
            "obtained_date",
            "validity",
            "file",
        )


class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = (
            "user",
            "vacancy",
            "status",
            "cover_letter",
            "remarks",
            "document",
            "submission_date",
        )


class VacancySerializer(ModelSerializer):
    class Meta:
        model = Vacancy
        fields = (
            "position",
            "town",
            "deadline",
            "is_published",
            "is_external",
            "remarks",
        )


class InterviewSerializer(ModelSerializer):
    class Meta:
        model = Interview
        fields = (
            "applicant",
            "dateTime",
            "status",
            "description",
            "location",
            "interview_type",
            "duration",
            "reschedule_reason",
            "reschedule_date",
            "rejection_reasons",
        )
