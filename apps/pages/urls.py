from django.urls import path
from .views import (
    ContactView,
    PoliciesView,
    TermsView,
    HomeView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("policies/", PoliciesView.as_view(), name="policies"),
    path("terms/", TermsView.as_view(), name="terms"),
]
