from django.contrib import admin

from .models import JobCompetency, CompetencyAnswer, Question, Category

admin.site.register(JobCompetency)
admin.site.register(CompetencyAnswer)
admin.site.register(Question)
admin.site.register(Category)