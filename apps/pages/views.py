from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from apps.recruitment.models import Vacancy, Bursary
from django.utils import timezone


class HomeView(TemplateView):
    template_name = "pages/home.html"


class AboutView(TemplateView):
    template_name = "pages/about.html"


class ContactView(TemplateView):
    template_name = "pages/contact.html"


class FaqView(TemplateView):
    template_name = "pages/faq.html"


class PoliciesView(TemplateView):
    template_name = "pages/policies.html"


class TermsView(TemplateView):
    template_name = "pages/terms.html"
