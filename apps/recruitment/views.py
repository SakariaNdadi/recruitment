from typing import Any
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    DetailView,
    TemplateView,
    UpdateView,
    ListView,
    View,
)
from django.contrib import messages
from utils.mixins import OwnerEditMixin
from .forms import (
    VacancyForm,
    ApplicationCreateForm,
    ApplicationEvaluationForm,
    InterviewForm,
    BursaryForm,
    BursaryApplicationForm,
)
from .models import Vacancy, Application, Interview, Bursary, BursaryApplication
from apps.accounts.models import Profile
from utils.mixins import OwnerMixin
from django.http import JsonResponse
from datetime import timedelta, datetime, timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class VacancyDetailView(DetailView):
    model = Vacancy
    context_object_name = "vacancy"
    template_name = "recruitment/vacancy/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        vacancy_id = self.kwargs["pk"]
        existing = Application.objects.filter(user=user, vacancy=vacancy_id)

        context["existing"] = existing
        return context


class VacancyCreateView(CreateView):
    form_class = VacancyForm
    template_name = "recruitment/vacancy/create.html"
    # success_url = None
    success_url = reverse_lazy("vacancy_create")


class VacancyUpdateView(UpdateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = "recruitment/vacancy/update.html"

    def get_success_url(self):
        return reverse_lazy("vacancy_detail", args=[self.object.pk])


def vacancies(request):
    now = datetime.now()
    bursaries = Bursary.objects.filter(is_published=True, deadline__gt=now)
    vacancies = Vacancy.objects.filter(is_published=True, deadline__gt=now)
    vacancies_is_external = vacancies.filter(is_external=True)
    vacancies_is_internal = vacancies.filter(is_external=False)
    bursaries_is_external = bursaries.filter(is_external=True)
    bursaries_is_internal = bursaries.filter(is_external=False)
    context = {
        "vacancies": vacancies,
        "bursaries": bursaries,
        "vacancies_is_external": vacancies_is_external,
        "vacancies_is_internal": vacancies_is_internal,
        "bursaries_is_external": bursaries_is_external,
        "bursaries_is_internal": bursaries_is_internal,
    }
    return render(request, "recruitment/vacancy/list.html", context)


def apply(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    user = request.user

    try:
        profile = Profile.objects.get(user=user)
        if (
            not profile.first_name
            or not profile.last_name
            or not profile.id_number
            or not profile.population_group
            or not profile.date_of_birth
            or not profile.primary_contact
            or not profile.cv
        ):
            messages.error(
                request,
                "Your profile is not complete. Please fill in all required fields.",
            )
            return redirect("profile_edit", request.user.pk)
    except:
        pass

    if request.method == "POST":
        form = ApplicationCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.vacancy = vacancy
            form.instance.user = user
            form.save()
            return redirect("vacancy_list")
        else:
            form = ApplicationCreateForm()
    form = ApplicationCreateForm
    return render(
        request,
        "recruitment/application_create.html",
        {"form": form, "vacancy": vacancy},
    )


class ApplicationDetailView(DetailView):
    model = Application
    context_object_name = "application"
    template_name = "recruitment/application/detail.html"


class ApplicationEvaluationView(UpdateView):
    model = Application
    form_class = ApplicationEvaluationForm
    template_name = "recruitment/application_evaluation.html"
    success_url = reverse_lazy("applications")

    # def get_success_url(self):
    #     return reverse_lazy("application_detail", args=[self.id])


class UserApplicationListView(OwnerMixin, ListView):
    model = Application
    context_object_name = "applications"
    template_name = "recruitment/application/list.html"


class ApplicationListView(ListView):
    model = Application
    context_object_name = "applications"
    template_name = "recruitment/application/list.html"


class InterviewCreateView(CreateView):
    model = Interview
    form_class = InterviewForm
    template_name = "recruitment/interview/create.html"
    success_url = reverse_lazy("interviews")

    def form_valid(self, form):
        form.instance.status = "scheduled"
        application = form.cleaned_data["application"]
        application.status = "scheduled"
        application.save()
        return super().form_valid(form)


class InterviewListView(ListView):
    model = Application
    context_object_name = "applications"
    template_name = "recruitment/interview/list.html"

    def get_queryset(self):
        # Filter applications directly in the query
        return Application.objects.filter(
            status="shortlisted",
        )


@method_decorator(csrf_exempt, name="dispatch")
class InterviewDataView(View):
    def get(self, request, *args, **kwargs):
        interviews = Interview.objects.all()
        interview_data = []
        for interview in interviews:
            interview_data.append(
                {
                    "id": interview.pk,
                    "title": f"{interview.application} Interview",
                    "start": interview.dateTime.isoformat(),
                    "end": (
                        interview.dateTime + timedelta(minutes=interview.duration)
                    ).isoformat(),
                    # 'url': reverse('interview_detail', args=[interview.pk]),
                }
            )
        return JsonResponse(interview_data, safe=False)


class InterviewDetailView(DetailView):
    model = Interview


class CalendarDataView(View):
    def get(self, request, *args, **kwargs):
        interviews = Interview.objects.all()
        events = []

        for interview in interviews:
            event = {
                "title": interview.application.user,  # Replace with the actual field representing the applicant's name
                "start": interview.dateTime.isoformat(),
                "end": (
                    interview.dateTime + timedelta(minutes=interview.duration)
                ).isoformat(),
                "description": interview.description,
                "location": interview.location,
                "status": interview.status,
            }
            events.append(event)

        return JsonResponse(events, safe=False)


class BursaryCreateView(CreateView):
    model = Bursary
    form_class = BursaryForm
    template_name = "recruitment/bursary/create.html"
    success_url = reverse_lazy("home")

    # def get_success_url(self):
    #     return super().get_success_url()


class BursaryUpdateView(UpdateView):
    model = Bursary
    form_class = BursaryForm
    template_name = "recruitment/bursary/update.html"
    success_url = reverse_lazy("home")

    # def get_success_url(self):
    #     return super().get_success_url()


class BursaryDetailView(DetailView):
    model = Bursary
    context_object_name = "bursary"
    template_name = "recruitment/bursary/detail.html"


class BursaryApplicationCreateView(OwnerEditMixin, CreateView):
    model = BursaryApplication
    form_class = BursaryApplicationForm
    template_name = "recruitment/bursary/application_create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        bursary_id = self.kwargs["pk"]
        user = self.request.user

        profile = Profile.objects.get(user=user)
        if (
            not profile.first_name
            or not profile.last_name
            or not profile.id_number
            or not profile.gender
            or not profile.population_group
            or not profile.date_of_birth
            or not profile.primary_contact
            or not profile.cv
            or not profile.is_created
        ):
            messages.error(
                self.request,
                "Your profile is not complete. Please fill in all required fields.",
            )
            return redirect("profile_edit", self.request.user.pk)

        form.instance.applicant_id = user.pk
        form.instance.bursary_id = bursary_id

        return super().form_valid(form)

    # def get_success_url(self):
    #     return super().get_success_url()


class BursaryApplicationDetailView(DetailView):
    model = BursaryApplication
    context_object_name = "bursary_application"
    template_name = "recruitment/bursary/application_detail.html"


class BursaryApplicationListView(ListView):
    model = BursaryApplication
    context_object_name = "bursary_applications"
    template_name = "recruitment/bursary/application_list.html"
