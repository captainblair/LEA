# lea_app/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Attendance, Center

# Define a common set of CSS classes for our form inputs
input_class = "appearance-none mt-1 relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:bg-gray-700"

class CustomUserCreationForm(UserCreationForm):
    """
    A form for new users to sign up. This version is simple and secure.
    It does NOT have a 'role' field, which was causing the error.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'center')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Add styling to the fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': input_class})

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture', 'center', 'role']

    def __init__(self, *args, **kwargs):
        viewing_user = kwargs.pop('user', None)
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name != 'profile_picture':
                self.fields[field_name].widget.attrs.update({'class': input_class})
        
        # If the user viewing this form is NOT an admin, hide the role field.
        if viewing_user and not viewing_user.is_admin:
            if 'role' in self.fields:
                self.fields['role'].widget = forms.HiddenInput()

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date', 'session_type', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': input_class}),
            'session_type': forms.Select(attrs={'class': input_class}),
            'status': forms.Select(attrs={'class': input_class}),
        }