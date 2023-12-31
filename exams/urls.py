from django.urls import path
from exams.apps import ExamsConfig
from exams.views import ExamView, ExamResultsView, ExamListView

app_name = ExamsConfig.name

urlpatterns = [
    path('exam/<int:exam_id>/', ExamView.as_view(), name='exam'),
    path(
        'exam/<int:exam_id>/results/',
        ExamResultsView.as_view(),
        name='exam_results'
    ),
    path('exams_list/', ExamListView.as_view(), name='exams_list'),
]
