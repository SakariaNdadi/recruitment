from django import forms
from .models import JobCompetency, Question, CompetencyAnswer


class JobCompetencyCreateForm(forms.ModelForm):
    class Meta:
        model = JobCompetency
        fields = (
            "employee",
            "position",
        )


class CompetencyAnswerCreateForm(forms.ModelForm):
    question = forms.CharField(disabled=True)
    class Meta:
        model = CompetencyAnswer
        fields = (
            "question",
        )
class EmployeeCompetencyAnswerCreateForm(CompetencyAnswerCreateForm):
    class Meta:
        model = CompetencyAnswer
        fields = (
            "employee_answer",
        )
class SupervisorCompetencyAnswerCreateForm(CompetencyAnswerCreateForm):
    class Meta:
        model = CompetencyAnswer
        fields = (
            "supervisor_answer",
        )