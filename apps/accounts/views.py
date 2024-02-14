from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from utils.mixins import OwnerEditMixin, OwnerMixin, get_user_type
from .models import Profile, Education, Experience, Certification
from .forms import (
    EducationCreateForm,
    ExperienceCreateForm,
    CertificationCreateForm,
    AdminUpdateForm,
    EmployeeUpdateForm,
    ApplicantUpdateForm,
    ProfileCreateBaseForm,
    EmployeeCreateForm,
    ApplicantCreateForm,
)
from django.contrib import messages
from django.contrib.auth import logout


# ***************************************************************************
class ProfileDetailView(OwnerMixin, DetailView):
    model = Profile
    context_object_name = "profile"
    template_name = "account/profile/detail.html"


class ProfileUpdateView(OwnerEditMixin, UpdateView):
    template_name = "account/profile/update.html"
    model = Profile

    def get_form_class(self):
        user_type = get_user_type(self.request.user)

        if user_type == "applicant":
            return ApplicantUpdateForm
        elif user_type in ["temp", "staff", "manager", "chief"]:
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
        return reverse_lazy("profile_detail", args=[self.pk])


class ProfileCreateView(OwnerMixin, CreateView):
    model = Profile
    template_name = "account/profile/create.html"
    form_class = ProfileCreateBaseForm

    def get_form(self, form_class=None):
        user_type = get_user_type(self.request.user)

        if user_type == "applicant":
            return ApplicantCreateForm(**self.get_form_kwargs())
        elif user_type in ["temp", "staff", "manager", "chief"]:
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


class CertificationCreateView(OwnerEditMixin, CreateView):
    form_class = CertificationCreateForm
    template_name = "account/profile/certification/create.html"

    def get_success_url(self):
        return reverse_lazy("profile_detail", args=[self.request.user.pk])


class CertificationDetailView(OwnerMixin, DetailView):
    model = Certification
    context_object_name = "certification"
    template_name = "account/profile/certification/detail.html"


class CertificationListView(OwnerMixin, ListView):
    model = Certification
    context_object_name = "certifications"
    template_name = "account/profile/certification/list.html"

    def get_queryset(self):
        return self.request.user.certification.all()


# ***************************************************************************


class EducationCreateView(OwnerEditMixin, CreateView):
    form_class = EducationCreateForm
    template_name = "account/profile/education/create.html"

    def get_success_url(self):
        return reverse_lazy("profile_detail", args=[self.request.user.pk])


class EducationDetailView(OwnerMixin, DetailView):
    model = Education
    context_object_name = "education"
    template_name = "account/profile/education/detail.html"


class EducationListView(OwnerMixin, ListView):
    model = Education
    context_object_name = "qualifications"
    template_name = "account/profile/education/list.html"

    def get_queryset(self):
        return self.request.user.education.all()

    # def get(self, request):
    #     return Education.objects.filter(user=request.user.pk)


# ***************************************************************************


class ExperienceCreateView(OwnerEditMixin, CreateView):
    form_class = ExperienceCreateForm
    template_name = "account/profile/experience/create.html"

    def get_success_url(self):
        return reverse_lazy("profile_detail", args=[self.request.user.pk])


class ExperienceDetailView(OwnerMixin, DetailView):
    model = Experience
    context_object_name = "experience"
    template_name = "account/profile/experience/detail.html"


class ExperienceListView(OwnerMixin, ListView):
    model = Experience
    context_object_name = "experiences"
    template_name = "account/profile/experience/list.html"

    def get_queryset(self):
        return self.request.user.experience.all()


# ***************************************************************************
