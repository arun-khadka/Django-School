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


# For fetching list of schools logged in or not
class SchoolListAPIView(APIView):
    """
    Returns a list of schools filtered by a search query (for autocomplete).
    """

    def get(self, request):
        query = request.query_params.get("q", "").strip()  # search query
        if query:
            schools = School.objects.filter(name__icontains=query).order_by("name")
        else:
            schools = School.objects.all().order_by("name")

        data = [{"id": school.id, "name": school.name} for school in schools]
        return Response(data, status=status.HTTP_200_OK)


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
