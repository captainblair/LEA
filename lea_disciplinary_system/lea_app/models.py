# lea_app/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    Includes a role-based system for permissions.
    """
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        COMMITTEE = 'COMMITTEE', 'Committee'
        MEMBER = 'MEMBER', 'Member'

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.MEMBER)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    center = models.ForeignKey('Center', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    # --- Helper Properties ---
    @property
    def is_admin(self):
        """Returns True if the user has the ADMIN role."""
        return self.role == self.Role.ADMIN

    # THIS IS THE NEW PROPERTY needed for the home page logic.
    # It defines "committee" access as either Committee or Admin role.
    @property
    def is_committee(self):
        """Returns True if the user is a Committee member or an Admin."""
        return self.role in [self.Role.COMMITTEE, self.Role.ADMIN]

    def __str__(self):
        """A string representation of the User model, used in the Django admin."""
        return self.username

# --- Other Application Models ---

class Center(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    SESSION_TYPES = [('physical', 'Physical'), ('online', 'Online'), ('meetup', 'Meetup')]
    STATUS_CHOICES = [('present', 'Present'), ('absent', 'Absent')]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    session_type = models.CharField(max_length=10, choices=SESSION_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f'{self.user.username} - {self.date} ({self.status})'

class DisciplinaryCase(models.Model):
    STATUS_CHOICES = [('open', 'Open'), ('reviewing', 'Reviewing'), ('closed', 'Closed')]

    accused = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases')
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Case for {self.accused.username}: {self.title}'