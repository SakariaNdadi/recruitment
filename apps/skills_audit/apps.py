from django.apps import AppConfig


class SkillsAuditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.skills_audit'

    def ready(self):
        import apps.skills_audit.signals
