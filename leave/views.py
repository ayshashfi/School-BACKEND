from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import LeaveApplication
from .serializers import LeaveApplicationSerializer
from django.http import Http404
from main.models import Student


class LeaveApplicationListCreateView(generics.ListCreateAPIView):
    """
    View for listing all leave applications and creating a new leave application
    """
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_student:
            raise Http404('User is not a student.')

        try:
            student = Student.objects.get(pk=user.pk)
        except Student.DoesNotExist:
            raise Http404('Student profile not found.')

        serializer.save(student=student)


class LeaveApplicationDetailView(generics.RetrieveAPIView):
    """
    View for retrieving a specific leave application
    """
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]


class IsAdminOrTeacher(permissions.BasePermission):
    """
    Custom permission to only allow access to admin or teacher users.
    """

    def has_permission(self, request, view):
        return request.user and (request.user.is_admin or request.user.is_teacher)


class UpdateLeaveStatusView(APIView):
    """
    Custom view to update the leave status by admin or teacher
    """
    permission_classes = [IsAdminOrTeacher]

    def patch(self, request, pk):
        try:
            leave = LeaveApplication.objects.get(pk=pk)
        except LeaveApplication.DoesNotExist:
            return Response({'error': 'Leave application not found'}, status=404)

        status = request.data.get('status')
        if status not in ['APPROVED', 'REJECTED']:
            return Response({'error': 'Invalid status'}, status=400)

        leave.status = status
        leave.save()
        return Response({'status': leave.status})
