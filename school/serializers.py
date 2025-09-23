from rest_framework import serializers
from school.models import School


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["id", "name", "address", "owner", "created_at"]
        read_only_fields = ["owner", "created_at"]
