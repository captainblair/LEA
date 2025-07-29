from datetime import date

def get_today():
    return date.today()

def calculate_attendance_percentage(attendance_queryset):
    total_days = attendance_queryset.count()
    present_days = attendance_queryset.filter(status='present').count()
    return (present_days / total_days) * 100 if total_days > 0 else 0
