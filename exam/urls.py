from django.urls import path
from .views import (
    AllMarksheetAPIView,
    ExamTermCreateView,
    ExamMarksheetGenerateView,
    ExamTermListBySchoolView,
    ExamTermListByUserView,
    ExamTermListView,
    MarksheetExportView,
    MarksheetImportView,
    SingleStudentMarksRetrieveView,
    StudentMarksRetrieveView,
)

urlpatterns = [
    path("terms/create/", ExamTermCreateView.as_view(), name="exam-term-create"),
    path("terms/list/", ExamTermListView.as_view(), name="exam-term-list"),
    path("terms/<int:school_id>/", ExamTermListBySchoolView.as_view(), name="exam-term-list-by-school"),
    path("terms/", ExamTermListByUserView.as_view(), name="exam-terms-by-user"),

    # Export blank marksheet via query params
    path("marksheet/export/", MarksheetExportView.as_view(), name="marksheet-export"),
    
    # Generate marksheet for a term/class/section
    path(
        "marksheet/generate/<int:term_id>/<int:class_id>/",
        ExamMarksheetGenerateView.as_view(),
        name="marksheet-generate",
    ),
    path(
        "marksheet/generate/<int:term_id>/<int:class_id>/<int:section_id>/",
        ExamMarksheetGenerateView.as_view(),
        name="marksheet-generate-section",
    ),

    # Uploads filled marksheet with marks and stores in db
    path("marksheet/import/", MarksheetImportView.as_view(), name="marksheet-import"),

    # NEW: Single student marksheet by OTP
    path("marksheet/single/", SingleStudentMarksRetrieveView.as_view(), name="marksheet-single-otp"),

    path("marksheet/all/", AllMarksheetAPIView.as_view(), name="marksheet-single-otp"),

    # For fetching all marksheets
    path(
        'student-marks/',
        StudentMarksRetrieveView.as_view(),
        name='student-marks-retrieve'
    ),
]
