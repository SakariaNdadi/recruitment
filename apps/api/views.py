from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from apps.accounts.models import Profile
from apps.recruitment.models import Application, Vacancy, Interview
from .serializers import (
    ProfileSerializer,
    ApplicationSerializer,
    VacancySerializer,
    InterviewSerializer,
)

# **********************************************************************************

class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# *********************************************************************************

class VacancyViewSet(ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
# *********************************************************************************
class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
# *********************************************************************************
class InterviewViewSet(ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
# *********************************************************************************
