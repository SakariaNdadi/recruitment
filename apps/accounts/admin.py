from django.contrib import admin
from .models import Profile, Education, Certification, Experience

admin.site.register(Experience)
admin.site.register(Certification)
admin.site.register(Education)
admin.site.register(Profile)
