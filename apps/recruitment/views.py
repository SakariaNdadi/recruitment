from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    ListView,
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
    ApplicationCreateForm,
)
from .models import (
    Vacancy,
    Application,
    Interview,
    Bursary,
    BursaryApplication,
)
from apps.accounts.models import Profile
from utils.mixins import OwnerMixin
from datetime import datetime
from .tasks import send_vacancy_application_notification_email, send_interview_notification_email


# ******************************************************************************************************
#                                     Vacancy Views
# ******************************************************************************************************
class VacancyCreateView(CreateView):
    form_class = VacancyForm
    template_name = "recruitment/vacancy/create.html"
    # success_url = None
    success_url = reverse_lazy("vacancy_create")

class VacancyDetailView(DetailView):
    model = Vacancy
    context_object_name = "vacancy"
    template_name = "recruitment/vacancy/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy_id = self.kwargs["pk"]
        user = self.request.user

        if user.is_authenticated:
            vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
            existing = Application.objects.filter(user=user, vacancy=vacancy).exists()
            context["existing"] = existing
        else:
            user = None

        context["vacancy_id"] = vacancy_id
        return context

class VacancyUpdateView(UpdateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = "recruitment/vacancy/update.html"

    def get_success_url(self):
        return reverse_lazy("vacancy_detail", args=[self.pk])


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



# ******************************************************************************************************
#                                     Application Views
# ******************************************************************************************************
class ApplicationDetailView(DetailView):
    model = Application
    context_object_name = "application"
    template_name = "recruitment/application/detail.html"


class ApplicationEvaluationView(UpdateView):
    model = Application
    form_class = ApplicationEvaluationForm
    template_name = "recruitment/application_evaluation.html"
    success_url = reverse_lazy("applications")


class ApplicationListView(ListView):
    model = Application
    context_object_name = "applications"
    template_name = "recruitment/application/list.html"

class ApplicationCreateView(CreateView):
    model = Application
    form_class = ApplicationCreateForm
    template_name = "recruitment/application/apply.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        vacancy_pk = self.kwargs.get("pk")
        user = self.request.user
        vacancy = get_object_or_404(Vacancy, pk=vacancy_pk)
        form.instance.vacancy = vacancy
        application_id = form.instance.id
        send_vacancy_application_notification_email.delay(application_id)
        return super().form_valid(form)
    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        vacancy_pk = self.kwargs.get("pk")
        user = self.request.user
        kwargs["vacancy_instance"] = get_object_or_404(Vacancy, pk=vacancy_pk)
        kwargs["user"] = user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy_pk = self.kwargs.get("pk")
        user = self.request.user
        vacancy = get_object_or_404(Vacancy, pk=vacancy_pk)

        if user and user.is_authenticated:
            existing = Application.objects.filter(user=user, vacancy=vacancy).exists()
            profile = Profile.objects.get(user=user)
            profile_complete = all(getattr(profile, field_name) for field_name in ['first_name', 'last_name', 'gender', 'id_number', 'population_group', 'date_of_birth', 'primary_contact'])
            
            context["existing"] = existing
            context["profile_complete"] = profile_complete
        else:
            context["existing"] = False
            context["profile_complete"] = True

        return context
    


@login_required
def my_applications(request):
    template_name = "recruitment/application/my_applications.html"
    applications = Application.objects.filter(user = request.user)
    context = {
        "applications": applications
    }
    return render(request,template_name, context)

class ApplicationListView(ListView):
    model = Application
    context_object_name = "applications"
    template_name = "recruitment/application/list.html"


# ******************************************************************************************************
#                                     Interview Views
# ******************************************************************************************************
class InterviewCreateView(CreateView):
    model = Interview
    form_class = InterviewForm
    template_name = "recruitment/interview/create.html"
    success_url = reverse_lazy("interview_list")

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
    
class InterviewDetailView(DetailView):
    model = Interview




# ******************************************************************************************************
#                                     Bursary Views
# ******************************************************************************************************
class BursaryCreateView(CreateView):
    model = Bursary
    form_class = BursaryForm
    template_name = "recruitment/bursary/create.html"
    success_url = reverse_lazy("home")

class BursaryUpdateView(UpdateView):
    model = Bursary
    form_class = BursaryForm
    template_name = "recruitment/bursary/update.html"
    success_url = reverse_lazy("home")


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


class BursaryApplicationDetailView(DetailView):
    model = BursaryApplication
    context_object_name = "bursary_application"
    template_name = "recruitment/bursary/application_detail.html"


class BursaryApplicationListView(ListView):
    model = BursaryApplication
    context_object_name = "bursary_applications"
    template_name = "recruitment/bursary/application_list.html"
