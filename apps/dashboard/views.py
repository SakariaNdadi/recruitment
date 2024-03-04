from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse, resolve
from subprocess import Popen
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import time
from django.utils import timezone
from datetime import timedelta, datetime
from apps.recruitment.models import Application, Vacancy

@login_required
def report_view(request):
    Popen(["streamlit", "run", "apps/dashboard/reports/main.py"])
    time.sleep(2)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def index(request):
    six_months_ago = timezone.now() - timedelta(days=30*6)
    now = datetime.now()
    template_name = "base.html"
    applications = Application.objects.filter(user = request.user, submission_date__range=[six_months_ago, timezone.now()])
    vacancies = Vacancy.objects.filter(is_published=True, deadline__gt=now)
    context = {
        "applications": applications,
        "vacancies": vacancies,
    }
    return render(request,template_name, context)