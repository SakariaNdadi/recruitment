from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    ProfileViewSet,EducationViewSet,ExperienceViewSet,CertificationViewSet,VacancyViewSet,ApplicationViewSet,InterviewViewSet
)

router = SimpleRouter()
router.register("profiles",ProfileViewSet, basename="profiles")
router.register("educations",EducationViewSet, basename="educations")
router.register("experiences",ExperienceViewSet, basename="experience")
router.register("certifications",CertificationViewSet, basename="certifications")
router.register("vacancies",VacancyViewSet, basename="vacancies")
router.register("applications",ApplicationViewSet, basename="applications")
router.register("interviews",InterviewViewSet, basename="interviews")
urlpatterns = router.urls