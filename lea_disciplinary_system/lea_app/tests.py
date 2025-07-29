from django.test import TestCase
from .models import User

class SimpleTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username='testuser', password='12345', role='member')
        self.assertEqual(user.username, 'testuser')
