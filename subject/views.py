from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from section.models import Section
from subject.serializers import SubjectSerializer
from django.shortcuts import get_object_or_404
from subject.models import Subject
from classes.models import Class
from .renderers import UserRenderer


class SubjectCreateView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SubjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        class_obj = serializer.validated_data["class_obj"]
        if class_obj.school.owner != request.user:
            return Response(
                {
                    "error": f"You do not own the school for class({class_obj.school.name})"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        subject = serializer.save()
        return Response(
            {
                "msg": "Subject created successfully",
                "subject": SubjectSerializer(subject).data,
            },
            status=status.HTTP_201_CREATED,
        )


class SubjectListView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, class_id, section_name=None, format=None):
        class_obj = get_object_or_404(Class, pk=class_id)

        # ✅ ownership check
        if class_obj.school.owner != request.user:
            return Response(
                {"error": "You do not own this school"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if section_name:
            section = Section.objects.filter(
                name=section_name, class_obj=class_obj
            ).first()
            if not section:
                return Response(
                    {"error": "Section not found in this class"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            subjects = Subject.objects.filter(class_obj=class_obj, section=section)
        else:
            subjects = Subject.objects.filter(class_obj=class_obj)

        serializer = SubjectSerializer(subjects, many=True)
        return Response(
            {"msg": "Subjects retrieved successfully", "subjects": serializer.data},
            status=status.HTTP_200_OK,
        )


class SubjectListByUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Fetch all subjects under schools owned by the logged-in user
        subjects = Subject.objects.filter(class_obj__school__owner=request.user) \
                                  .select_related("class_obj", "section", "class_obj__school")
        serializer = SubjectSerializer(subjects, many=True)
        return Response(
            {
                "msg": "Subjects retrieved successfully",
                "subjects": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class SubjectDeleteView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        try:
            subject = Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            return Response(
                {"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if subject.class_obj.school.owner != request.user:
            return Response(
                {"error": "You do not own this school"},
                status=status.HTTP_403_FORBIDDEN,
            )

        subject.delete()
        return Response(
            {"msg": "Subject deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
