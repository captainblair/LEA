# lea_app/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Center, Attendance, DisciplinaryCase

# We need to create a custom admin view for our custom User model
class CustomUserAdmin(UserAdmin):
    # Add our custom fields to the list displays and fieldsets
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role', 'center')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'center')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'center')}),
    )

# Register your models here so they appear in the admin panel
admin.site.register(User, CustomUserAdmin)
admin.site.register(Center)
admin.site.register(Attendance)
admin.site.register(DisciplinaryCase)