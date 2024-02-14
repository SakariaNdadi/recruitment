from django.shortcuts import redirect
from subprocess import Popen
import time

def report_view(request):
    Popen(["streamlit", "run", "apps/dashboard/reports/main.py"])
    time.sleep(2)
    return redirect("vacancy_list")
