from django.views.generic import (
    View,
)
from .models import (
    Interview,
)
from django.http import JsonResponse
from datetime import timedelta
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name="dispatch")
class InterviewDataView(View):
    def get(self, request, *args, **kwargs):
        interviews = Interview.objects.all()
        interview_data = []
        for interview in interviews:
            interview_data.append(
                {
                    "id": interview.pk,
                    "title": f"{interview.application} Interview",
                    "start": interview.dateTime.isoformat(),
                    "end": (
                        interview.dateTime + timedelta(minutes=interview.duration)
                    ).isoformat(),
                    # 'url': reverse('interview_detail', args=[interview.pk]),
                }
            )
        return JsonResponse(interview_data, safe=False)