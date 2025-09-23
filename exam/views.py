from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import openpyxl
from openpyxl.utils import get_column_letter
from django.shortcuts import get_object_or_404
from exam.utils.all_marksheet import get_all_students_marksheet_data
from exam.utils.marksheet_generator import generate_blank_marksheet
from rest_framework.parsers import MultiPartParser

from exam.utils.single_marksheet import get_single_student_marksheet_data
from school.models import School
from subject.models import Subject
from classes.models import Class
from section.models import Section
from django.http import HttpResponse
from .models import ExamTerm

from .serializers import ExamTermSerializer
from .serializers import MarksheetImportSerializer
from .utils.marksheet_importer import generate_marksheet_with_results


class ExamTermCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ExamTermSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the school from validated data
        school = serializer.validated_data.get("school")
        if not school:
            return Response(
                {"error": "School is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Ownership check
        if school.owner != request.user:
            return Response(
                {"error": "You do not own this school"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Save the term
        term = serializer.save()
        return Response(
            {
                "msg": "Exam term created successfully",
                "term": ExamTermSerializer(term).data,
            },
            status=status.HTTP_201_CREATED,
        )


class ExamTermListByUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all terms linked to schools owned by the logged-in user
        terms = ExamTerm.objects.filter(school__owner=request.user).select_related("school")

        serializer = ExamTermSerializer(terms, many=True)
        return Response(
            {
                "msg": "Exam terms retrieved successfully",
                "terms": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    

class ExamTermListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch only terms for schools owned by logged-in user
        terms = ExamTerm.objects.filter(school__owner=request.user)
        serializer = ExamTermSerializer(terms, many=True)
        return Response(
            {"msg": "Exam terms retrieved successfully", "terms": serializer.data},
            status=status.HTTP_200_OK,
        )


class ExamTermListBySchoolView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, school_id):
        # Verify school ownership
        try:
            school = School.objects.get(id=school_id, owner=request.user)
        except School.DoesNotExist:
            return Response(
                {"error": "School not found or you do not own this school"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Fetch terms for this school
        terms = ExamTerm.objects.filter(school=school)
        serializer = ExamTermSerializer(terms, many=True)
        return Response(
            {"msg": "Exam terms retrieved successfully", "terms": serializer.data},
            status=status.HTTP_200_OK,
        )


class MarksheetExportView(APIView):
    """
    Export a blank marksheet for manual entry.
    Query params: school (id), class (id), section (id, optional), term (id)
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get query parameters
            school_id = request.query_params.get("school")
            class_id = request.query_params.get("class")
            section_id = request.query_params.get("section")
            term_id = request.query_params.get("term")

            # Validate required params
            if not school_id or not class_id or not term_id:
                return Response(
                    {"error": "school, class, and term are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Fetch school and check ownership
            school = get_object_or_404(School, id=school_id)
            if school.owner != request.user:
                return Response(
                    {"error": "You do not own this school"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Fetch class and term
            class_obj = get_object_or_404(Class, id=class_id, school=school)
            term = get_object_or_404(ExamTerm, id=term_id, school=school)

            # Fetch section if provided
            section_obj = None
            if section_id:
                section_obj = get_object_or_404(Section, id=section_id, school=school)

            # Fetch subjects according to class and section
            subjects = Subject.objects.filter(class_obj=class_obj)
            if section_obj:
                subjects = subjects.filter(section=section_obj)
            else:
                subjects = subjects.filter(section__isnull=True)

            # Check if subjects exist
            if not subjects.exists():
                return Response(
                    {"error": "No subjects found for the selected class/section"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Generate Excel file
            return generate_blank_marksheet(
                school, class_obj, section_obj, term, subjects
            )

        except Exception as e:
            # Catch any unexpected error
            return Response(
                {"error": f"Internal server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ExamMarksheetGenerateView(APIView):
    """
    Generate an Excel marksheet for a specific term, class, and optional section.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, term_id, class_id, section_id=None):
        # Fetch exam term, ensuring it belongs to logged-in user's school
        term = get_object_or_404(ExamTerm, id=term_id, school__owner=request.user)

        # Fetch class and optional section
        class_obj = get_object_or_404(Class, id=class_id, school=term.school)

        section_obj = None
        if section_id:
            section_obj = get_object_or_404(Section, id=section_id, class_obj=class_obj)

        # Get subjects for class/section
        subjects = Subject.objects.filter(class_obj=class_obj)
        if section_obj:
            subjects = subjects.filter(section=section_obj)

        # Create workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"{term.name} Marksheet"

        # Header row
        headers = ["S.N.", "Name", "Roll No", "OTP"] + [sub.name for sub in subjects]
        for col_num, header in enumerate(headers, 1):
            col_letter = get_column_letter(col_num)
            ws[f"{col_letter}1"] = header

        # Pre-fill 50 empty rows for manual entry
        for row_num in range(2, 52):
            ws[f"A{row_num}"] = row_num - 1  # SN auto-fill
            ws[f"D{row_num}"] = ""  # OTP column left blank for admin to fill

        # Send file as response
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        filename = f"{term.name}_{class_obj.grade}"
        if section_obj:
            filename += f"_{section_obj.name}"
        filename += "_marksheet.xlsx"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        wb.save(response)
        return response


class MarksheetImportView(APIView):
    """
    Import an Excel marksheet, calculate pass/fail, and export styled Excel
    """

    def post(self, request):
        serializer = MarksheetImportSerializer(data=request.data)
        if serializer.is_valid():
            full_mark = serializer.validated_data["full_mark"]
            pass_mark = serializer.validated_data["pass_mark"]
            file = serializer.validated_data["file"]

            try:
                return generate_marksheet_with_results(file, full_mark, pass_mark)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleMarksheetAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get("file")
        otp_input = request.data.get("otp")

        if not file or not otp_input:
            return Response(
                {"error": "File and OTP are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            data = get_single_student_marksheet_data(file, otp_input)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_200_OK)


class AllMarksheetAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "File is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            data = get_all_students_marksheet_data(file)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_200_OK)