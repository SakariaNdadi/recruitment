from django.urls import path
from .views import (
    QuestionsListView,
    JobCompetencyProfiles,
    EmployeeCompetencyProfiles,
    EmployeeCompetencyDetailView,
    question_create,
    delete_question,
    delete_all_question,
    search_question,
    search_question_create,
    filter_category_question,
    my_skills_audit
)

urlpatterns = [
    path("my-skills_audit", my_skills_audit, name="my_skills_audit"),
    path("job-competency/profiles/", JobCompetencyProfiles.as_view(), name="job_competency_list"),
    path("employee-competency/profiles/", EmployeeCompetencyProfiles.as_view(), name="employee_competency_list"),
    path(
        "job-competency-profile/questions/list/<int:jcp_id>/",
        QuestionsListView.as_view(),
        name="job_competency_profile_questions_list",
    ),
    path(
        "employee-competency-profile/list/",
        EmployeeCompetencyProfiles.as_view(),
        name="employee_competency_profile_list",
    ),
    path(
        "employee-competency-profile/detail/<int:pk>/",
        EmployeeCompetencyDetailView.as_view(),
        name="employee_competency_profile_detail",
    ),
]

htmx_urlpatterns = [
    path("add_question/", question_create, name="add_question"),
    path("delete_question/<int:pk>/", delete_question, name="delete_question"),
    path(
        "delete_all_question/<int:pk>/", delete_all_question, name="delete_all_question"
    ),
    path("search_question/<int:pk>/", search_question, name="search_question"),
    path(
        "search_question_create/", search_question_create, name="search_question_create"
    ),
    path(
        "filter_category_question/<int:pk>/",
        filter_category_question,
        name="filter_category_question",
    ),
]

urlpatterns += htmx_urlpatterns
