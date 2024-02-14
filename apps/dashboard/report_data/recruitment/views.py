from django.views.generic import View
from apps.recruitment.models import Application, Vacancy, BursaryApplication, Interview
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse

@method_decorator(csrf_exempt, name="dispatch")
class VacancyDataView(View):
    def get(self, request, *args, **kwargs):
        vacancies = Vacancy.objects.all()
        vacancy_data = []
        for vacancy in vacancies:
            vacancy_data.append(
                {
                    "id": vacancy.pk,
                    "position": f"{vacancy.position}",
                    "town": f"{vacancy.town}",
                    "is_published": f"{vacancy.is_published}",
                    "is_external": f"{vacancy.is_external}",
                    "deadline": vacancy.deadline.isoformat(),
                }
            )
        return JsonResponse(vacancy_data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class VacancyApplicationDataView(View):
    def get(self, request, *args, **kwargs):
        applications = Application.objects.all()
        application_data = []
        for application in applications:
            application_data.append(
                {
                    "id": application.pk,
                    "user": f"{application.user.email}",
                    "vacancy": f"{application.vacancy}",
                    "gender": f"{application.user.profile.gender}",
                    "date_of_birth": f"{application.user.profile.date_of_birth}",
                    "vacancy": f"{application.vacancy.position.title}",
                    "status": f"{application.status}",
                    "submission_date": application.submission_date.strftime("%Y-%m-%dT%H:%M"),
                }
            )
        return JsonResponse(application_data, safe=False)

@method_decorator(csrf_exempt, name="dispatch")
class BursaryApplicantDataView(View):
    def get(self, request, *args, **kwargs):
        bursaries = BursaryApplication.objects.all()
        bursary_data = []
        for bursary in bursaries:
            bursary_data.append(
                {
                    "bursary": bursary.bursary.title,
                    "applicant": f"{bursary.applicant}",
                    "gender": f"{bursary.applicant.profile.gender}",
                    "date_of_birth": f"{bursary.applicant.profile.date_of_birth}",
                    "status": f"{bursary.status}",
                    "field_of_study": f"{bursary.field_of_study}",
                    "institute": f"{bursary.institute}",
                    "mode_of_study": f"{bursary.mode_of_study}",
                    "minimum_study_duration": f"{bursary.minimum_study_duration}",
                    "maximum_study_duration": f"{bursary.maximum_study_duration}",
                    "tuition_fees": f"{bursary.tuition_fees}",
                    "travel_fees": f"{bursary.travel_fees}",
                    "accommodation_fees": f"{bursary.accommodation_fees}",
                    "books_fees": f"{bursary.books_fees}",
                    "other_fees": f"{bursary.other_fees}",
                    "first_year_total_fees": f"{bursary.first_year_total_fees}",
                    "gross_total_all_years": f"{bursary.gross_total_all_years}",
                    "submission_date": bursary.submission_date.isoformat(),
                }
            )
        return JsonResponse(bursary_data, safe=False)