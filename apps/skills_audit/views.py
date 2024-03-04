from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import JobCompetency, Question, Category, CompetencyAnswer
from .forms import (
    JobCompetencyCreateForm,
    EmployeeCompetencyAnswerCreateForm,
    SupervisorCompetencyAnswerCreateForm,
)
from utils.mixins import OwnerEditMixin



@login_required
def my_skills_audit(request):
    template_name = "skills_audit/my_skills_audit.html"
    return render(request,template_name)

# ******************************************************************************************************
#                                     JOB COMPETENCY PROFILE VIEWS
# ******************************************************************************************************

class JobCompetencyProfiles(LoginRequiredMixin, ListView):
    model = JobCompetency
    context_object_name = "jcps"
    template_name = "skills_audit/job_competency/list.html"

    def get_queryset(self):
        user_position = self.request.user.profile.position

        if not user_position:
            return JobCompetency.objects.none()

        if self.request.user.profile.user_type == "chief":
            return JobCompetency.objects.filter(
                position__division=user_position.division
            )
        else:
            return JobCompetency.objects.filter(position__line_manager=user_position)

class JobCompetencyProfilesCreateView(LoginRequiredMixin, CreateView):
    model = JobCompetency
    form_class = JobCompetencyCreateForm
    template_name = "skills_audit/jcp/create.html"
    success_url = "jcps"


class QuestionsListView(LoginRequiredMixin, ListView):
    model = Question
    context_object_name = "questions"
    template_name = "skills_audit/jcp/detail.html"

    def get_queryset(self):
        jcp_id = self.kwargs.get("jcp_id")
        return Question.objects.filter(job_competency=jcp_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jcp_id = self.kwargs.get("jcp_id")
        categories = Category.objects.filter(
            questions__job_competency=jcp_id
        ).distinct()
        context["jcp"] = JobCompetency.objects.get(pk=jcp_id)
        context["categories"] = Category.objects.all()
        context["search_category"] = categories
        return context


@login_required
def question_create(request):
    jcp_id = request.POST.get("jcp_id") or request.GET.get("jcp_id")
    text = request.POST.get("text")
    category_id = request.POST.get("category")
    job_competency = JobCompetency.objects.filter(pk=jcp_id).first()
    category = get_object_or_404(Category, pk=category_id)
    question = Question.objects.get_or_create(
        text=text, category=category, job_competency=job_competency
    )[0]
    questions = Question.objects.filter(job_competency=job_competency)
    context = {"questions": questions}
    return render(request, "skills_audit/jcp/partials/question_list.html", context)


@login_required
@require_http_methods(["DELETE"])
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.delete()
    jcp = question.job_competency
    questions = Question.objects.filter(job_competency=jcp)
    context = {"questions": questions}
    return render(request, "skills_audit/jcp/partials/question_list.html", context)


@login_required
@require_http_methods(["DELETE"])
def delete_all_question(request, pk):
    jcp = get_object_or_404(JobCompetency, pk=pk)
    jcp.questions.all().delete()
    questions = Question.objects.filter(job_competency=jcp)
    context = {"questions": questions}
    return render(request, "skills_audit/jcp/partials/question_list.html", context)


@login_required
def search_question(request, pk):
    jcp = get_object_or_404(JobCompetency, pk=pk)
    search_text = request.POST.get("search_question")
    questions = Question.objects.filter(job_competency=jcp, text__icontains=search_text)
    context = {
        "questions": questions,
    }
    return render(request, "skills_audit/jcp/partials/question_list.html", context)


@login_required
def search_question_create(request):
    jcp_id = request.POST.get("jcp_id") or request.GET.get("jcp_id")
    jcp = get_object_or_404(JobCompetency, pk=jcp_id)
    jcp_questions = jcp.questions.all()

    search_text = request.POST.get("text")
    questions = Question.objects.filter(text__icontains=search_text).exclude(
        text__in=jcp_questions.values_list("text", flat=True)
    )
    context = {
        "questions": questions,
    }
    return render(request, "skills_audit/jcp/partials/question_list.html", context)


@login_required
def filter_category_question(request, pk):
    jcp = get_object_or_404(JobCompetency, pk=pk)
    categories = request.POST.getlist("category_filter")
    questions = Question.objects.filter(job_competency=jcp, category__in=categories)
    context = {"questions": questions}
    return render(request, "skills_audit/jcp/partials/question_list.html", context)


# ******************************************************************************************************
#                                     EMPLOYEE COMPETENCY PROFILE VIEWS
# ******************************************************************************************************

class EmployeeCompetencyDetailView(LoginRequiredMixin, DetailView):
    model = JobCompetency
    context_object_name = "jcp"
    template_name = "skills_audit/ecp/detail.html"


class EmployeeCompetencyProfiles(LoginRequiredMixin, ListView):
    model = CompetencyAnswer
    context_object_name = "ecps"
    template_name = "skills_audit/employee_competency/list.html"

    def get_queryset(self):
        user_position = self.request.user.profile.position

        if not user_position:
            return JobCompetency.objects.none()

        if self.request.user.profile.user_type == "chief":
            return JobCompetency.objects.filter(
                position__division=user_position.division
            )
        else:
            return JobCompetency.objects.filter(position__line_manager=user_position)