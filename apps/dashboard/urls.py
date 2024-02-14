from django.urls import path
from .views import (
    report_view
)

from .report_data.accounts.urls import accounts_urlpatterns
from .report_data.recruitment.urls import recruitment_urlpatterns
urlpatterns = [
    path("reports/", report_view, name="charts"),
]

urlpatterns += accounts_urlpatterns
urlpatterns += recruitment_urlpatterns