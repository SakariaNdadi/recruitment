from django.urls import path
from .views import (
    report_view,
    index,
)

from .report_data.accounts.urls import accounts_urlpatterns
from .report_data.recruitment.urls import recruitment_urlpatterns
urlpatterns = [
    path("", index, name="dashboard"),
    path("reports/", report_view, name="reports"),
]

urlpatterns += accounts_urlpatterns
urlpatterns += recruitment_urlpatterns