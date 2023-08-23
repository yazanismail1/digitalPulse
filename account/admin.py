from django.contrib import admin

from account.models import CustomUser, UserProfile

admin.site.register(CustomUser)
admin.site.register(UserProfile)
