from django.urls import path
from .views import (
    VacancyCreateView,
    VacancyUpdateView,
    VacancyDetailView,
    vacancies,
    ApplicationEvaluationView,
    UserApplicationListView,
    ApplicationListView,
    ApplicationDetailView,
    InterviewCreateView,
    InterviewListView,
    InterviewDetailView,
    CalendarDataView,
    InterviewDataView,
    BursaryCreateView,
    BursaryDetailView,
    BursaryUpdateView,
    BursaryApplicationCreateView,
    BursaryApplicationDetailView,
    BursaryApplicationListView,
    apply,
)

urlpatterns = [
    path("vacancy/create/", VacancyCreateView.as_view(), name="vacancy_create"),
    path("vacancy/update/<int:pk>", VacancyUpdateView.as_view(), name="vacancy_update"),
    path("vacancies/", vacancies, name="vacancy_list"),
    path("vacancy/<int:pk>/", VacancyDetailView.as_view(), name="vacancy_detail"),
    path("application/<int:pk>/", apply, name="apply"),
    path(
        "application/<int:pk>",
        ApplicationDetailView.as_view(),
        name="application_detail",
    ),
    path(
        "application/evaluation/<int:pk>/",
        ApplicationEvaluationView.as_view(),
        name="application_evaluation",
    ),
    path(
        "my-applications/", UserApplicationListView.as_view(), name="user_applications"
    ),
    path("applications/", ApplicationListView.as_view(), name="applications"),
    path("interviews/", InterviewListView.as_view(), name="interviews"),
    path("interviews/create/", InterviewCreateView.as_view(), name="interview_create"),
    path("interview_data", InterviewDataView.as_view(), name="interview_data"),
    path(
        "interviews/detail/<int:pk>",
        InterviewDetailView.as_view(),
        name="interview_detail",
    ),
    path("calendar_data/", CalendarDataView.as_view(), name="calendar_data"),
    path("bursary/create/", BursaryCreateView.as_view(), name="bursary_create"),
    path(
        "bursary/detail/<int:pk>/", BursaryDetailView.as_view(), name="bursary_detail"
    ),
    path(
        "bursary/update/<int:pk>/", BursaryUpdateView.as_view(), name="bursary_update"
    ),
    path(
        "bursary/apply/<int:pk>/",
        BursaryApplicationCreateView.as_view(),
        name="apply_bursary",
    ),
    path(
        "bursary/application/detail/<int:pk>/",
        BursaryApplicationDetailView.as_view(),
        name="bursary_application_detail",
    ),
    path(
        "bursary/application/list/",
        BursaryApplicationListView.as_view(),
        name="bursary_application_list",
    ),
]
