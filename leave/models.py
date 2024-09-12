# leaves/models.py

from django.db import models
from django.conf import settings
from main.models import Student 

class LeaveApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),

    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE,null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.start_date} to {self.end_date} ({self.status})"
