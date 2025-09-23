from rest_framework import serializers
from classes.models import Class
from school.models import School
from section.models import Section


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'name']  # adjust fields as needed


class ClassSerializer(serializers.ModelSerializer):
    # Show school name
    school = serializers.CharField(source="school.name", read_only=True)
    
    # Accept school by name on create/update
    school_slug = serializers.SlugRelatedField(
        slug_field="name",
        queryset=School.objects.all(),
        write_only=True,
        source="school",
    )

    # Include sections in the output (read-only)
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Class
        fields = [
            "id",
            "school",        # read-only school name
            "school_slug",   # write-only school name for create/update
            "grade",
            "created_at",
            "sections",      # nested sections
        ]
        read_only_fields = ["id", "school", "created_at", "sections"]
