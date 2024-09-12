from django.db import models
from main.models import ClassRoom, Subject, Teacher, Student

class ExamType(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

class Syllabus(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.classroom} - {self.subject} - {self.teacher}'
    
    def get_dataa(self):
        return f'{self.subject.subject} - {self.teacher.username}'
    
    class Meta:
        ordering = ['classroom__class_no', 'classroom__section']

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, blank=True, null=True)  
    assignment_mark = models.IntegerField()
    exam_mark = models.IntegerField()
    exam_date = models.DateField(null=True)
    submitted_by = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'exam_type', 'syllabus', 'exam_date'], name='unique_student_syllabus_examtype')
        ]

    def __str__(self):
        return f'{self.student} - {self.syllabus}  - {self.assignment_mark} - {self.exam_mark}'
