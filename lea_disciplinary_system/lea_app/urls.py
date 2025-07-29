# lea_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Public & User URLs
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'), # Added signup
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('profile/', views.profile_view, name='profile'),
    
    # Admin URLs - THE VISION
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/members/', views.members_view, name='members'),
    
    # **NEW URL for the member detail page**
    path('admin/members/<int:user_id>/', views.admin_member_detail_view, name='admin_member_detail'),
    
    path('admin/reports/', views.reports_view, name='reports'),
    path('admin/settings/', views.settings_view, name='settings'),
]