from django.urls import path
from .views import (
    ResultCreateView, ResultListView, ResultDetailView,
    SyllabusListView, SyllabusDetailView, SyllabusByClassroomView,
    ExamTypeView, ExamTypeDetailView
)

urlpatterns = [
    path('', ResultCreateView.as_view(), name='result-list-create'),
    path('<int:id>/', ResultDetailView.as_view(), name='result-detail'),
    path('results/', ResultListView.as_view(), name='result_list'),
    path('syllabus/', SyllabusListView.as_view(), name='syllabus-list'),
    path('syllabus/<int:id>/', SyllabusDetailView.as_view(), name='syllabus-detail'),  
    path('syllabus_by_class/<int:id>/', SyllabusByClassroomView.as_view(), name='syllabus_by_class'),
    path('exam_type/', ExamTypeView.as_view(), name='exam_type_list_create'),
    path('exam_type/<int:id>/', ExamTypeDetailView.as_view(), name='exam_type_detail'),
]
