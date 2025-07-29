from rest_framework import serializers
from .models import User, Attendance, DisciplinaryCase

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class DisciplinaryCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplinaryCase
        fields = '__all__'
