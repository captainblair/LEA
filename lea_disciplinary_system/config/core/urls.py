# config/core/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import your custom view for login
from lea_app import views as lea_app_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- YOUR CUSTOM LOGIN URL ---
    # This comes FIRST, so it overrides the default login URL from the include below.
    # This is correct and should be kept.
    path('accounts/login/', lea_app_views.custom_login_view, name='login'),
    
    # --- INCLUDE ALL OTHER DJANGO AUTH URLS ---
    # This is the NEW and IMPORTANT line.
    # It automatically adds URLs for logout, password_change, password_reset, etc.
    # Any URL that starts with 'accounts/' and isn't your custom login will be handled here.
    path('accounts/', include('django.contrib.auth.urls')),

    # Your app's main URLs
    path('', include('lea_app.urls')),
]

# This is for serving user-uploaded files (like profile pictures) during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)