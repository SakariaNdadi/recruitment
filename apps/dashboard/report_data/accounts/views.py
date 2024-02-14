from django.views.generic import View
from apps.accounts.models import Profile
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

@method_decorator(csrf_exempt, name="dispatch")
class ProfileDataView(View):
    def get(self, request, *args, **kwargs):
        # profiles = Profile.objects.filter(user_type__in = ["manager", "applicant"])
        profiles = Profile.objects.exclude(user_type="applicant")
        profile_data = []

        for profile in profiles:

            position_data = {
                "position": "N/A",
                "division": "N/A",
            }

            if profile.position:
                position_data["position"] = f"{profile.position}"
                if profile.position.division:
                    position_data["division"] = f"{profile.position.division}"


            profile_data.append(
                {
                    # "id": profile.pk,
                    "first_name": f"{profile.first_name}",
                    "last_name": f"{profile.last_name}",
                    "user_type": f"{profile.user_type}",
                    "nationality": f"{profile.nationality}",
                    "population_group": f"{profile.population_group}",
                    "gender": f"{profile.gender}",
                    "date_of_birth": f"{profile.date_of_birth}",
                    "position": f"{profile.position}",
                    # "division": f"{profile.position.division}",
                    **position_data,
                    "call_center_number": f"{profile.call_center_number}",
                    "appointed_date": profile.appointed_date,
                    # "created": profile.created.isoformat(),
                }
            )
        return JsonResponse(profile_data, safe=False)
