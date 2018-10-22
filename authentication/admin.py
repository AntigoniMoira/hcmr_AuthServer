"""
Customize admin interface.
"""
from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    """
    Settings for UserProfile admin table.
    """
    list_display = ['user', 'userPhone', 'birthDate',
                    'gender', 'country', 'institution', 'description']
    search_fields = ['user', 'userPhone', 'birthDate',
                     'gender', 'country', 'institution', 'description']
    list_per_page = 10

admin.site.register(UserProfile, UserProfileAdmin)
