from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from classes.models import Class
from classes.renderers import UserRenderer
from classes.serializers import ClassSerializer
from school.models import School


class ClassCreateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ClassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        school = serializer.validated_data["school"]

        if not school:
            return Response(
                {"error": "School field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check ownership safely
        if not hasattr(school, "owner"):
            return Response(
                {"error": "School model has no owner field"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if school.owner != request.user:
            return Response(
                {"error": "You do not own this school"},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            serializer.save()

        except Exception as e:
            return Response(
                {"error": f"Failed to create class: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"msg": "Class created successfully!", "class": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class ClassListView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            classes = (
                Class.objects.filter(school__owner=request.user)
                .select_related("school")  # fetch school in same query
                .prefetch_related("sections")  # fetch sections efficiently
            )
            serializer = ClassSerializer(classes, many=True)
            return Response(
                {"msg": "Classes retrieved successfully", "classes": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ClassListBySchoolView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # You can provide either school_id or school_name as query params
        school_id = request.query_params.get("school_id")
        school_name = request.query_params.get("school_name")

        if not school_id and not school_name:
            return Response(
                {"error": "Provide school_id or school_name as query parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch school owned by the logged-in user
        try:
            if school_id:
                school = School.objects.get(id=school_id, owner=request.user)
            else:
                school = School.objects.get(name=school_name, owner=request.user)
        except School.DoesNotExist:
            return Response(
                {"error": "School not found or you do not own this school"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Fetch all classes for this school
        classes = Class.objects.filter(school=school)
        serializer = ClassSerializer(classes, many=True)

        return Response(
            {"msg": "Classes retrieved successfully", "classes": serializer.data},
            status=status.HTTP_200_OK,
        )


class ClassRetrieveView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            class_obj = Class.objects.get(pk=pk)
        except Class.DoesNotExist:
            return Response(
                {"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Check ownership
        if class_obj.school.owner != request.user:
            return Response(
                {"error": "You do not own this school"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ClassSerializer(class_obj)
        return Response(
            {"msg": "Class retrieved successfully", "class": serializer.data},
            status=status.HTTP_200_OK,
        )


class ClassUpdateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        try:
            class_obj = Class.objects.get(pk=pk)
        except Class.DoesNotExist:
            return Response(
                {"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if class_obj.school.owner != request.user:
            return Response(
                {"error": "You do not own this school"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ClassSerializer(class_obj, data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(
            {"msg": "Class updated successfully", "class": serializer.data},
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk, format=None):
        try:
            class_obj = Class.objects.get(pk=pk)
        except Class.DoesNotExist:
            return Response(
                {"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if class_obj.school.owner != request.user:
            return Response(
                {"error": "You do not own this school"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ClassSerializer(class_obj, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(
            {"msg": "Class updated successfully", "class": serializer.data},
            status=status.HTTP_200_OK,
        )


class ClassDeleteView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        try:
            class_obj = Class.objects.get(pk=pk)
        except Class.DoesNotExist:
            return Response(
                {"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if class_obj.school.owner != request.user:
            return Response(
                {"error": "You do not own this school"},
                status=status.HTTP_403_FORBIDDEN,
            )

        class_obj.delete()
        return Response(
            {"msg": "Class deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
