from rest_framework.serializers import ModelSerializer
from apps.accounts.models import Profile
from apps.recruitment.models import Application, Vacancy, Interview


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "user",
            "first_name",
            "last_name",
            "date_of_birth",
            "id_number",
            "primary_contact",
            "secondary_contact",
            "gender",
            "population_group",
            "postal_address",
            "linkedin",
            "picture",
            "cv",
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
            "application",
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
