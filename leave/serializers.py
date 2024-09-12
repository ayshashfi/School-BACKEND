from rest_framework import serializers
from .models import LeaveApplication
from main.serializers import StudentSerializer
from main.models import Student

class LeaveApplicationSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())  # Accepts an ID for input

    # To include nested student data in the output
    student_detail = StudentSerializer(source='student', read_only=True)

    class Meta:
        model = LeaveApplication
        fields = ['id', 'student', 'student_detail', 'start_date', 'end_date', 'reason', 'status']
