from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from apps.recruitment.models import Vacancy, Bursary
from datetime import timedelta, datetime, timezone
from .forms import ContactForm
from django.urls import reverse_lazy
class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        return context
    


class ContactView(CreateView):
    template_name = "pages/partials/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("home")


class PoliciesView(TemplateView):
    template_name = "pages/policies.html"


class TermsView(TemplateView):
    template_name = "pages/terms.html"
