from django.contrib import admin
from .models import Department,Division,Position, Qualification, Certification


class DivisionInline(admin.TabularInline):
    model = Division

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "chief",
    ]
    list_filter = [
        "name",
    ]
    inlines = [DivisionInline]

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "job_grade",
        "division",
    ]
    list_filter = [
        "title",
        "job_grade",
        "division",
        "qualification",
    ]

@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = [
        "type",
        "title",
    ]
    list_filter = [
        "type",
        "title",
    ]

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "level",
    ]
    list_filter = [
        "title",
        "title",
    ]