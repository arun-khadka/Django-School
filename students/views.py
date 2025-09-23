from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from students.models import Student, StudentMarks, StudentSubjectMarks
from students.serializers import (
    StudentSerializer,
    StudentMarksSerializer,
    StudentSubjectMarksSerializer,
)


class StudentListCreateView(APIView):
    """
    GET: List all students
    POST: Create a new student
    """

    def get(self, request, *args, **kwargs):
        queryset = Student.objects.all().order_by("class_obj", "section", "roll_no")
        serializer = StudentSerializer(queryset, many=True)
        return Response(
            {"count": queryset.count(), "students": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response(
                {
                    "message": "Student created successfully",
                    "student": StudentSerializer(student).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentListView(APIView):
    """
    GET: List all students (read-only)
    """

    def get(self, request, *args, **kwargs):
        queryset = Student.objects.all().order_by("class_obj", "section", "roll_no")
        serializer = StudentSerializer(queryset, many=True)
        return Response(
            {"count": queryset.count(), "students": serializer.data},
            status=status.HTTP_200_OK,
        )


class StudentMarksListCreateView(APIView):
    """
    GET: List all student marks
    POST: Create new student marks entry
    """

    def get(self, request, *args, **kwargs):
        queryset = StudentMarks.objects.all().order_by(
            "student__class_obj", "student__section", "student__roll_no"
        )
        serializer = StudentMarksSerializer(queryset, many=True)
        return Response(
            {"count": queryset.count(), "student_marks": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        serializer = StudentMarksSerializer(data=request.data)
        if serializer.is_valid():
            student_marks = serializer.save()
            return Response(
                {
                    "message": "Student marks created successfully",
                    "student_marks": StudentMarksSerializer(student_marks).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentSubjectMarksListCreateView(APIView):
    """
    GET: List all student subject marks
    POST: Create new student subject marks entry
    """

    def get(self, request, *args, **kwargs):
        queryset = StudentSubjectMarks.objects.all().order_by(
            "student_marks__student__class_obj",
            "student_marks__student__section",
            "student_marks__student__roll_no",
        )
        serializer = StudentSubjectMarksSerializer(queryset, many=True)
        return Response(
            {"count": queryset.count(), "subject_marks": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        serializer = StudentSubjectMarksSerializer(data=request.data)
        if serializer.is_valid():
            subject_mark = serializer.save()
            return Response(
                {
                    "message": "Student subject marks created successfully",
                    "subject_mark": StudentSubjectMarksSerializer(subject_mark).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
