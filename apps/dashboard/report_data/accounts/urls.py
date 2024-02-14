from django.urls import path
from .views import ProfileDataView

accounts_urlpatterns = [
    path("profile_data/", ProfileDataView.as_view()),
]
