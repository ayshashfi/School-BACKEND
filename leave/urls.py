# leaves/urls.py

from django.urls import path
from .views import LeaveApplicationListCreateView, LeaveApplicationDetailView, UpdateLeaveStatusView

urlpatterns = [
    path('leave-applications/', LeaveApplicationListCreateView.as_view(), name='leave-application-list-create'),
    path('leave-applications/<int:pk>/', LeaveApplicationDetailView.as_view(), name='leave-application-detail'),
    path('leave-applications/<int:pk>/update-status/', UpdateLeaveStatusView.as_view(), name='update-leave-status'),
]
