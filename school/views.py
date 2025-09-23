from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from school.models import School

from school.renderers import UserRenderer
from school.serializers import SchoolSerializer


class SchoolCreateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = SchoolSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(
            {"msg": "School created successfully", "school": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class SchoolListView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Get all schools owned by the logged-in user
        schools = School.objects.filter(owner=request.user)
        serializer = SchoolSerializer(schools, many=True)
        return Response(
            {"msg": "Schools retrieved successfully", "schools": serializer.data},
            status=status.HTTP_200_OK,
        )
