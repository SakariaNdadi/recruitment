from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from apps.accounts.models import Profile, Education, Experience, Certification
from apps.recruitment.models import Application, Vacancy, Interview
from .serializers import (
    ProfileSerializer,
    EducationSerializer,
    ExperienceSerializer,
    CertificationSerializer,
    ApplicationSerializer,
    VacancySerializer,
    InterviewSerializer,
)

# **********************************************************************************

class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# *********************************************************************************

class EducationViewSet(ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
# *********************************************************************************

class ExperienceViewSet(ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
# *********************************************************************************

class CertificationViewSet(ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
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
