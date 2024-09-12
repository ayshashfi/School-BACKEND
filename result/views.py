# views.py
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ExamType, Result, Syllabus
from .serializers import ResultSerializer, SyllabusSerializer
from django.shortcuts import get_object_or_404
from main.serializers import ClassroomSerializer
from main.models import ClassRoom, Student
from rest_framework.permissions import IsAdminUser
from .serializers import ExamTypeSerializer
from django.db import IntegrityError


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Syllabus 
from .serializers import SyllabusSerializer
from rest_framework.exceptions import NotFound

class ResultCreateView(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

def create(self, request, *args, **kwargs):
    data = request.data
    serializer = ResultSerializer(data=data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            if 'unique_student_syllabus_examtype' in str(e):
                return Response({"error": "This combination of values already exists."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "An unexpected database error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResultDetailView(generics.ListAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    lookup_field = 'id'  # Using 'id' to match your URL pattern

    def get_object(self):
        student_id = self.kwargs.get('id')
        try:
            return Result.objects.filter(student_id=student_id)
        except Result.DoesNotExist:
            raise NotFound(detail="Result not found")


class ResultListView(generics.ListAPIView):
    serializer_class = ResultSerializer

    def get_queryset(self):
        syllabus_id = self.request.query_params.get('syllabusId', None)
        if syllabus_id is not None:
            return Result.objects.filter(syllabus_id=syllabus_id)
        return Result.objects.none()

class SyllabusListView(generics.ListCreateAPIView):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer


class TeacherClassListView(generics.ListAPIView):
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            return ClassRoom.objects.filter(classsubjectteacher__teacher=user)
        return ClassRoom.objects.none()
    
class ExamTypeView(generics.ListCreateAPIView):
    queryset = ExamType.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ExamTypeSerializer

class ExamTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExamType.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ExamTypeSerializer

class SyllabusByClassroomView(generics.ListAPIView):
    serializer_class = SyllabusSerializer

    def get_queryset(self):
        # Retrieve the 'id' from the URL parameters (assuming it's passed as part of the URL)
        classroom_id = self.kwargs.get('id')  # 'id' should match the name in your URL pattern

        try:
            class_room = ClassRoom.objects.get(id=classroom_id)
        except ClassRoom.DoesNotExist:
            raise NotFound(detail="ClassRoom not found")

        # Filter the Syllabus objects based on the classroom
        return Syllabus.objects.filter(classroom=class_room)
    

class SyllabusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
    # permission_classes = [IsAuthenticated]