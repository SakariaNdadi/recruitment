from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.contrib import messages
from django.urls import reverse_lazy
from utils.mixins import OwnerEditMixin, OwnerMixin, get_user_type
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import (
    AdminUpdateForm,
    EmployeeUpdateForm,
    ProfileCreateBaseForm,
    EmployeeCreateForm,
)
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin

# ******************************************************************************************************
#                                       PROFILE VIEWS
# ******************************************************************************************************
class ProfileDetailView(LoginRequiredMixin,DetailView):
    model = Profile
    context_object_name = "profile"
    template_name = "account/profile/detail.html"

@login_required
def my_profile(request):
    template_name = "account/profile/detail.html"
    return render(request,template_name)

class ProfileUpdateView(OwnerEditMixin, UpdateView):
    template_name = "account/profile/update.html"
    model = Profile

    def get_form_class(self):
        user_type = get_user_type(self.request.user)

        if user_type in ["temp", "staff", "manager", "chief"]:
            return EmployeeUpdateForm
        elif user_type == "admin":
            return AdminUpdateForm

        return None

    def get_form(self, form_class=None):
        form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.instance = self.request.user.profile
        response = super().form_valid(form)
        messages.success(self.request, "Profile Updated Successfully")
        return response

    def get_success_url(self):
        return reverse_lazy("profile_detail", args=[self.request.user.pk])


class ProfileCreateView(OwnerMixin, CreateView):
    model = Profile
    template_name = "account/profile/create.html"
    form_class = ProfileCreateBaseForm

    def get_form(self, form_class=None):
        user_type = get_user_type(self.request.user)

        if user_type in ["temp", "staff", "manager", "chief"]:
            return EmployeeCreateForm(**self.get_form_kwargs())

        return None

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()

        self.request.user.profile.is_created = True
        self.request.user.profile.save()

        if self.request.user.is_authenticated and hasattr(self.request, 'session'):
            logout(self.request)

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("account_login")


class ProfileListView(ListView):
    model = Profile
    context_object_name = "profiles"
    template_name = "account/profile/list.html"
    paginate_by = 50

# ***************************************************************************
