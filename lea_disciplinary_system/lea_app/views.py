# lea_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.db.models import Count, Exists, OuterRef
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings


from .models import User, Attendance, DisciplinaryCase, Center
from .forms import CustomUserCreationForm, AttendanceForm, ProfileUpdateForm
from .decorators import admin_required

# --- AUTHENTICATION & PUBLIC VIEWS ---
def custom_login_view(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('admin_dashboard')
        else:
            return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            if user.is_admin:
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def home(request):
    """
    Displays the public home page with dynamic, organization-wide statistics.
    THIS VIEW IS NOW UPGRADED TO POWER THE HOME PAGE.
    """
    total_members = User.objects.count()
    non_compliant_users = DisciplinaryCase.objects.filter(status__in=['open', 'reviewing']).values('accused').distinct().count()
    
    if total_members > 0:
        compliance_rate = round(((total_members - non_compliant_users) / total_members) * 100)
    else:
        compliance_rate = 100

    today_attendance_present = Attendance.objects.filter(date=date.today(), status='present').count()

    stats = {
        'total_members': total_members,
        'compliance_rate': compliance_rate,
        'non_compliant': non_compliant_users,
        'today_attendance': {
            'present': today_attendance_present,
            'total': total_members,
        }
    }
    context = {'stats': stats}
    return render(request, 'home.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# --- STANDARD USER VIEWS ---
@login_required
def dashboard_view(request):
    """
    Displays a personalized dashboard for the logged-in user.
    This version is now CORRECTED to fetch and display the recent attendance list properly.
    """
    user = request.user
    
    # --- Get Required Session Counts from settings.py ---
    physical_total = settings.PHYSICAL_SESSIONS_REQUIRED
    online_total = settings.ONLINE_SESSIONS_REQUIRED
    meetups_total = settings.MEETUP_SESSIONS_REQUIRED

    # --- Data Calculations ---
    compliance_status = not DisciplinaryCase.objects.filter(accused=user, status__in=['open', 'reviewing']).exists()
    
    user_attendance_records = Attendance.objects.filter(user=user, status='present')
    physical_attended = user_attendance_records.filter(session_type='physical').count()
    online_attended = user_attendance_records.filter(session_type='online').count()
    meetups_attended = user_attendance_records.filter(session_type='meetup').count()

    physical_percentage = (physical_attended / physical_total) * 100 if physical_total > 0 else 0
    online_percentage = (online_attended / online_total) * 100 if online_total > 0 else 0
    meetups_percentage = (meetups_attended / meetups_total) * 100 if meetups_total > 0 else 0
    
    # --- Chart Data ---
    thirty_days_ago = date.today() - timedelta(days=30)
    attendance_for_chart = Attendance.objects.filter(user=user, date__gte=thirty_days_ago).order_by('date')
    chart_labels = [att.date.strftime("%b %d") for att in attendance_for_chart]
    chart_data = [1 if att.status == 'present' else 0 for att in attendance_for_chart]

    # =======================================================
    # THE CRUCIAL FIX IS HERE
    # We must fetch a separate, clean list for the "Recent Attendance" section.
    # We order by date descending to get the newest ones first.
    # =======================================================
    recent_attendance_list = Attendance.objects.filter(user=user).order_by('-date')[:5]
    
    context = {
        'compliance_status': compliance_status,
        'physical_attended': physical_attended,
        'physical_total': physical_total,
        'physical_percentage': physical_percentage,
        'online_attended': online_attended,
        'online_total': online_total,
        'online_percentage': online_percentage,
        'meetups_attended': meetups_attended,
        'meetups_total': meetups_total,
        'meetups_percentage': meetups_percentage,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        # We pass the NEW, CORRECT list to the template
        'recent_attendance_list': recent_attendance_list,
    }
    
    return render(request, 'user/dashboard.html', context)
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user, user=request.user)
    context = {'form': form}
    return render(request, 'user/profile.html', context)

@login_required
def attendance_view(request):
    """
    Handles the form for marking attendance.
    THIS VERSION IS NOW CORRECTED TO:
    1. Show validation errors if the form is invalid.
    2. Redirect to the DASHBOARD on success for immediate confirmation.
    """
    # This logic handles both GET requests and invalid POST requests
    form = AttendanceForm()
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            # Check for duplicates before trying to save
            date_to_check = form.cleaned_data['date']
            if Attendance.objects.filter(user=request.user, date=date_to_check).exists():
                messages.warning(request, f'You have already submitted attendance for {date_to_check}.')
                return redirect('attendance') # Stay on the page to correct

            # If no duplicate, proceed to save
            attendance = form.save(commit=False)
            attendance.user = request.user
            attendance.save()
            messages.success(request, f'Attendance for {date_to_check} submitted successfully!')
            
            # THE CRUCIAL FIX: Redirect to the dashboard to see the result!
            return redirect('dashboard')

        # If form is NOT valid, the code will continue to the render below,
        # and the `form` variable will now contain the errors to be displayed.

    # This part runs for initial page loads (GET) and for when the form is invalid (POST)
    recent_attendances = Attendance.objects.filter(user=request.user).order_by('-date')[:5]
    context = {
        'form': form, # This is either a blank form or a form with errors
        'recent_attendances': recent_attendances
    }
    return render(request, 'user/attendance.html', context)

# --- ADMIN VIEWS ---
@login_required
@admin_required
def admin_dashboard_view(request):
    total_members = User.objects.count()
    non_compliant_users = DisciplinaryCase.objects.filter(status__in=['open', 'reviewing']).values('accused').distinct().count()
    compliance_rate = round(((total_members - non_compliant_users) / total_members) * 100) if total_members > 0 else 100
    today_attendance_present = Attendance.objects.filter(date=date.today(), status='present').count()
    stats = {'total_members': total_members, 'compliance_rate': compliance_rate, 'non_compliant': non_compliant_users, 'today_attendance': {'present': today_attendance_present, 'total': total_members}}
    thirty_days_ago = date.today() - timedelta(days=30)
    date_range = [date.today() - timedelta(days=i) for i in range(30)]
    attendance_counts = {dt.strftime("%b %d"): 0 for dt in sorted(date_range)}
    db_counts = Attendance.objects.filter(date__gte=thirty_days_ago, status='present').values('date').annotate(count=Count('id')).order_by('date')
    for item in db_counts:
        key = item['date'].strftime("%b %d")
        if key in attendance_counts:
            attendance_counts[key] = item['count']
    chart_labels = list(attendance_counts.keys())
    chart_data = list(attendance_counts.values())
    recent_attendance = Attendance.objects.order_by('-date', '-timestamp')[:5].select_related('user')
    context = {'stats': stats, 'chart_labels': chart_labels, 'chart_data': chart_data, 'recent_attendance': recent_attendance}
    return render(request, 'admin/dashboard.html', context)

@login_required
@admin_required
def members_view(request):
    all_members = User.objects.exclude(id=request.user.id).order_by('first_name', 'last_name')
    context = {'members': all_members}
    return render(request, 'admin/members.html', context)

@login_required
@admin_required
def admin_member_detail_view(request, user_id):
    member = get_object_or_404(User, id=user_id)
    compliance_status = not DisciplinaryCase.objects.filter(accused=member, status__in=['open', 'reviewing']).exists()
    thirty_days_ago = date.today() - timedelta(days=30)
    attendance_for_chart = Attendance.objects.filter(user=member, date__gte=thirty_days_ago).order_by('date')
    chart_labels = [att.date.strftime("%b %d") for att in attendance_for_chart]
    chart_data = [1 if att.status == 'present' else 0 for att in attendance_for_chart]
    recent_attendance = Attendance.objects.filter(user=member).order_by('-date')[:5]
    context = {'member': member, 'compliance_status': compliance_status, 'chart_labels': chart_labels, 'chart_data': chart_data, 'recent_attendance': recent_attendance}
    return render(request, 'admin/member_detail.html', context)

@login_required
@admin_required
def reports_view(request):
    return render(request, 'admin/reports.html')
    
@login_required
@admin_required
def settings_view(request):
    return render(request, 'admin/settings.html')