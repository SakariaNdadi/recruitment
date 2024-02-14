from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from apps.accounts.models import Profile

class OwnerMixin(LoginRequiredMixin):
    """
        Mixin to filter querysets based on the currently logged-in user.
    """
    user_attribute = 'user'
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(**{self.user_attribute: self.request.user})


class OwnerEditMixin(LoginRequiredMixin):
    """
        Mixin to set the user attribute of a form instance to the current user before form validation.
    """
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def get_user_type(user):
    try:
        profile = Profile.objects.get(user=user)
        return profile.user_type
    except Profile.DoesNotExist:
        return None
    
# class AccessControlMixin(LoginRequiredMixin):
#     def is_admin(self):
#         return self.request.user.profile.user_type == "admin"
    
#     def is_chief(self):
#         return self.request.user.profile.user_type == "chief"
    
#     def is_manager(self):
#         return self.request.user.profile.user_type == "manager"
    
#     def is_supervisor(self):
#         return self.request.user.profile.user_type == "supervisor"
    
#     def can_view_department(self, department):
#         if self.is_admin():
#             return True
#         elif self.is_chief() and department.chief == self.request.user:
#             return True
        
#         return False
        
#     def can_view_division(self, division):
#         if self.is_admin():
#             return True
#         elif self.is_chief() and division.department.chief == self.request.user:
#             return True
#         elif self.is_manager() and division.manager == self.request.user:
#             return True
#         return False
    
class AccessControlMixin(LoginRequiredMixin):
    def is_admin(self):
        return self.request.user.profile.user_type == "admin"
    
    def is_chief(self):
        return self.request.user.profile.user_type == "chief"
    
    def is_manager(self):
        return self.request.user.profile.user_type == "manager"
    
    def is_supervisor(self):
        return self.request.user.profile.user_type == "supervisor"
    
    def can_view_department_or_division(self, obj):
        if self.is_admin():
            return True
        elif self.is_chief() and obj.chief == self.request.user:
            return True
        elif self.is_manager() and obj.manager == self.request.user:
            return True
        else:
            return False
    
    def can_view_department(self, department):
        return self.can_view_department_or_division(department)
        
    def can_view_division(self, division):
        return self.can_view_department_or_division(division)