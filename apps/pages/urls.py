from django.urls import path
from .views import (
    AboutView,
    ContactView,
    FaqView,
    PoliciesView,
    TermsView,
    HomeView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("faq/", FaqView.as_view(), name="faq"),
    path("policies/", PoliciesView.as_view(), name="policies"),
    path("terms/", TermsView.as_view(), name="terms"),
]
