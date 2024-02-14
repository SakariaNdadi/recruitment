from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def user_first_login(request):
    if request.user.profile.first_login:
        return redirect("create_profile")
    else:
        return redirect("home")