from rest_framework import serializers
from section.models import Section
from classes.models import Class
from school.models import School

class SectionSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_obj.grade', read_only=True)
    school_name = serializers.CharField(source='school.name', read_only=True)

    class_obj_id = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(),
        write_only=True,
        source='class_obj'
    )

    class Meta:
        model = Section
        fields = [
            'id',
            'name',
            'class_obj_id',   # ✅ input
            'class_name',     # ✅ read-only
            'school',         # ✅ FK (read-only)
            'school_name',    # ✅ read-only
            'created_at'
        ]
        read_only_fields = ['id', 'school', 'class_name', 'school_name', 'created_at']

