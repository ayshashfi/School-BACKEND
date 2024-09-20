from rest_framework import serializers
from main.models import Student, Teacher
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.username', read_only=True)  # Assuming 'name' is the field for Teacher's name

    class Meta:
        model = Attendance
        fields = ['student', 'date', 'present', 'teacher', 'teacher_name']  # Include teacher_name in fields

    def validate(self, data):
        student = data.get('student')
        date = data.get('date')

        # Check if attendance already exists for the student and date
        if Attendance.objects.filter(student=student, date=date).exists():
            raise serializers.ValidationError(
                {"unique": "Attendance already marked."}
            )

        return data
