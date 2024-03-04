from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group
from django.core.management.base import BaseCommand
from apps.elearning.models import Course, Content, Module


class Command(BaseCommand):
    help = "Create groups and permissions"

    def handle(self, *args, **options):

        course_content_type = ContentType.objects.get_for_model(Course)
        content_content_type = ContentType.objects.get_for_model(Content)
        module_content_type = ContentType.objects.get_for_model(Content)

        # Course
        permission_add_course, created = Permission.objects.get_or_create(
            codename="add_course",
            name="Can add course",
            content_type=course_content_type,
        )
        permission_view_course, created = Permission.objects.get_or_create(
            codename="view_course",
            name="Can view course",
            content_type=course_content_type,
        )
        permission_edit_course, created = Permission.objects.get_or_create(
            codename="edit_course",
            name="Can edit course",
            content_type=course_content_type,
        )
        permission_delete_course, created = Permission.objects.get_or_create(
            codename="delete_course",
            name="Can delete course",
            content_type=course_content_type,
        )

        # Module
        permission_add_module, created = Permission.objects.get_or_create(
            codename="add_module",
            name="Can add module",
            content_type=module_content_type,
        )
        permission_view_module, created = Permission.objects.get_or_create(
            codename="view_module",
            name="Can view module",
            content_type=module_content_type,
        )
        permission_edit_module, created = Permission.objects.get_or_create(
            codename="edit_module",
            name="Can edit module",
            content_type=module_content_type,
        )
        permission_delete_module, created = Permission.objects.get_or_create(
            codename="delete_module",
            name="Can delete module",
            content_type=module_content_type,
        )

        # Content
        permission_add_content, created = Permission.objects.get_or_create(
            codename="add_content",
            name="Can add content",
            content_type=content_content_type,
        )
        permission_view_content, created = Permission.objects.get_or_create(
            codename="view_content",
            name="Can view content",
            content_type=content_content_type,
        )
        permission_edit_content, created = Permission.objects.get_or_create(
            codename="edit_content",
            name="Can edit content",
            content_type=content_content_type,
        )
        permission_delete_content, created = Permission.objects.get_or_create(
            codename="delete_content",
            name="Can delete content",
            content_type=content_content_type,
        )

        group_instructor, created = Group.objects.get_or_create(name="Instructor")

        group_instructor.permissions.add(
            permission_view_course,
            permission_add_course,
            permission_edit_course,
            permission_delete_course,
            permission_add_module,
            permission_edit_module,
            permission_view_module,
            permission_delete_module,
            permission_add_content,
            permission_edit_content,
            permission_view_content,
            permission_delete_content
        )

        self.stdout.write(
            self.style.SUCCESS("E-learning Groups and permissions created successfully.")
        )
