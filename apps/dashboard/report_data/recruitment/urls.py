from django.urls import path
from .views import VacancyDataView, VacancyApplicationDataView, BursaryApplicantDataView

recruitment_urlpatterns = [
    path("vacancy_data/",VacancyApplicationDataView.as_view()),
    path("bursary_applicant_data/",BursaryApplicantDataView.as_view()),
]
