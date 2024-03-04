from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    ProfileViewSet, VacancyViewSet,ApplicationViewSet,InterviewViewSet
)

router = SimpleRouter()
router.register("profiles",ProfileViewSet, basename="profiles")
router.register("vacancies",VacancyViewSet, basename="vacancies")
router.register("applications",ApplicationViewSet, basename="applications")
router.register("interviews",InterviewViewSet, basename="interviews")
urlpatterns = router.urls