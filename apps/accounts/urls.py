from django.urls import path
from .views import (
    ProfileDetailView,
    ProfileCreateView,
    ProfileUpdateView,
    ProfileListView,
)

urlpatterns = [
    path("profiles/", ProfileListView.as_view(), name="profile_list"),
    path(
        "profile/<int:pk>/",
        ProfileDetailView.as_view(),
        name="profile_detail",
    ),
    path(
        "profile/create/<int:pk>/",
        ProfileCreateView.as_view(),
        name="profile_create",
    ),
    path(
        "profile/update/<int:pk>/",
        ProfileUpdateView.as_view(),
        name="profile_update",
    ),
]
