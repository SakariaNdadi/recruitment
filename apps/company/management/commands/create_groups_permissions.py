from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group
from django.core.management.base import BaseCommand
from apps.company.models import Department, Division


class Command(BaseCommand):
    help = "Create groups and permissions"

    def handle(self, *args, **options):

        department_content_type = ContentType.objects.get_for_model(Department)
        division_content_type = ContentType.objects.get_for_model(Division)

        permission_add_department, created = Permission.objects.get_or_create(
            codename="add_department",
            name="Can add department",
            content_type=department_content_type,
        )
        permission_view_department, created = Permission.objects.get_or_create(
            codename="view_department",
            name="Can view department",
            content_type=department_content_type,
        )
        permission_edit_department, created = Permission.objects.get_or_create(
            codename="edit_department",
            name="Can edit department",
            content_type=department_content_type,
        )
        permission_delete_department, created = Permission.objects.get_or_create(
            codename="delete_department",
            name="Can delete department",
            content_type=department_content_type,
        )

        permission_add_division, created = Permission.objects.get_or_create(
            codename="add_division",
            name="Can add division",
            content_type=division_content_type,
        )
        permission_view_division, created = Permission.objects.get_or_create(
            codename="view_division",
            name="Can view division",
            content_type=division_content_type,
        )
        permission_edit_division, created = Permission.objects.get_or_create(
            codename="edit_division",
            name="Can edit division",
            content_type=division_content_type,
        )
        permission_delete_division, created = Permission.objects.get_or_create(
            codename="delete_division",
            name="Can delete division",
            content_type=division_content_type,
        )

        group_admin, created = Group.objects.get_or_create(name="Admin")
        group_chief, created = Group.objects.get_or_create(name="Chief")
        group_manager, created = Group.objects.get_or_create(name="Manager")
        group_supervisor, created = Group.objects.get_or_create(name="Supervisor")

        group_admin.permissions.add(
            permission_view_department,
            permission_add_department,
            permission_edit_department,
            permission_delete_department,
            permission_add_division,
            permission_edit_division,
            permission_view_division,
            permission_delete_division,
        )
        group_chief.permissions.add(permission_view_department)
        group_manager.permissions.add(permission_view_division)

        self.stdout.write(
            self.style.SUCCESS("Company Groups and permissions created successfully.")
        )
