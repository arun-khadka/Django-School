from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from school.models import School
from section.models import Section
from section.renderers import UserRenderer
from section.serializers import SectionSerializer
from classes.models import Class

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from section.models import Section
from section.serializers import SectionSerializer
from classes.models import Class
from school.models import School


# Create a Section
class SectionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        class_obj = serializer.validated_data.get("class_obj")
        if not class_obj:
            return Response({"error": "Class is required"}, status=400)

        # Ensure ownership via class → school
        if class_obj.school.owner != request.user:
            return Response({"error": "You do not own this school"}, status=403)

        # Save section with school inferred from class
        section = serializer.save(school=class_obj.school)
        return Response(
            {
                "msg": "Section created successfully",
                "section": SectionSerializer(section).data,
            },
            status=201,
        )


class SectionListBySchoolClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, school_id, class_id, format=None):
        # Verify school ownership
        try:
            school = School.objects.get(id=school_id, owner=request.user)
        except School.DoesNotExist:
            return Response(
                {"error": "School not found or you do not own this school"}, status=404
            )

        # Verify class belongs to this school
        try:
            class_obj = Class.objects.get(id=class_id, school=school)
        except Class.DoesNotExist:
            return Response({"error": "Class not found in this school"}, status=404)

        # Fetch sections
        sections = Section.objects.filter(school=school, class_obj=class_obj)
        serializer = SectionSerializer(sections, many=True)
        return Response(
            {"msg": "Sections retrieved successfully", "sections": serializer.data},
            status=200,
        )
    

class SectionListAllView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Fetch all sections for schools owned by the user
        sections = Section.objects.filter(class_obj__school__owner=request.user).select_related("class_obj")
        serializer = SectionSerializer(sections, many=True)
        return Response(
            {"msg": "Sections with classes retrieved successfully", "sections": serializer.data},
            status=status.HTTP_200_OK,
        )
    

class SectionListByClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, school_id, class_id, format=None):
        # Get class and verify ownership
        try:
            class_obj = Class.objects.get(
                id=class_id, school__id=school_id, school__owner=request.user
            )
        except Class.DoesNotExist:
            return Response(
                {"error": "Class not found or you do not own this school"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Fetch sections linked to this class
        sections = Section.objects.filter(class_obj=class_obj)
        serializer = SectionSerializer(sections, many=True)
        return Response(
            {"msg": "Sections retrieved successfully", "sections": serializer.data},
            status=status.HTTP_200_OK,
        )
