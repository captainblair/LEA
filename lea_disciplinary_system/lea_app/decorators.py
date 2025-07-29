# lea_app/decorators.py

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

def admin_required(function=None, redirect_field_name=None, login_url='login'):
    """
    Decorator for views that checks that the user is logged in and is an admin.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.role == 'admin',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator