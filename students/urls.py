from django.urls import path
from students.views import (
    StudentListCreateView,
    StudentListView,
    StudentMarksListCreateView,
    StudentSubjectMarksListCreateView,
)

urlpatterns = [
    path("create/", StudentListCreateView.as_view(), name="student-list-create"),
    path("list/", StudentListView.as_view(), name="student-list"),

    path(
        "student-marks/",
        StudentMarksListCreateView.as_view(),
        name="student-marks-list-create",
    ),
    path(
        "student-subject-marks/",
        StudentSubjectMarksListCreateView.as_view(),
        name="student-subject-marks-list-create",
    ),
]
