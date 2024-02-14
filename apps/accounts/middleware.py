from django.shortcuts import redirect
from django.urls import reverse


class ProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the user is authenticated and the profile is not created
        if (
            request.user.is_authenticated
            and not request.user.profile.is_created
            and request.path
            not in [
                reverse("profile_create", args=[request.user.pk]),
                reverse("account_logout"),
            ]
            and not request.path.startswith("/admin/")
        ):
            # Redirect to the profile_create page
            return redirect(reverse("profile_create", args=[request.user.pk]))

        return response
