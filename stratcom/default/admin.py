from django.contrib import admin
from .models import UserProfile, InternshipApplications, Gallery
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(InternshipApplications)
admin.site.register(Gallery)
