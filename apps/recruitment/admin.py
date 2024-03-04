from django.contrib import admin
from .models import (
    Region,
    Town,
    Vacancy,
    Application,
    Interview,
    Bursary,
    BursaryApplication,
)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = [
        "position",
        "town",
        "deadline",
        "is_published",
        "is_external",
    ]
    list_filter = [
        "town__region",
        "is_published",
        "is_external",
        "deadline",
    ]
    list_editable = [
        "is_published",
        "is_external",
    ]
    search_fields = ["position"]
    raw_id_fields = ["position"]


class TownInline(admin.TabularInline):
    model = Town
    raw_id_fields = [
        "region",
    ]


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]

    inlines = [
        TownInline,
    ]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "vacancy",
        "status",
        "submission_date",
    ]


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = [
        "application_email",
        "dateTime",
        "status",
        "interview_type",
        "duration",
    ]

    def application_email(self, obj):
        # Define a custom method to display the application's email
        return obj.application.email

    application_email.short_description = (
        "Applicant Email"  # Set a user-friendly column header
    )
    list_filter = [
        "dateTime",
        "status",
        "interview_type",
    ]
    list_editable = [
        "dateTime",
        "interview_type",
        "duration",
    ]
    raw_id_fields = ["application"]


admin.site.register(Bursary)


@admin.register(BursaryApplication)
class BursaryApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "bursary",
        "applicant",
        "status",
        "submission_date",
    ]
