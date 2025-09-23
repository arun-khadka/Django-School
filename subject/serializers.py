from rest_framework import serializers
from subject.models import Subject
from classes.models import Class
from section.models import Section

class SubjectSerializer(serializers.ModelSerializer):
    # Writeable fields
    class_obj = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    section = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.all(),
        allow_null=True,
        required=False
    )

    # Read-only fields for representation
    class_name = serializers.SerializerMethodField()
    section_name = serializers.SerializerMethodField()
    school_name = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            "id",
            "name",
            "class_obj",
            "class_name",
            "section",
            "section_name",
            "school_name",
            "created_at"
        ]
        read_only_fields = ["id", "class_name", "section_name", "school_name", "created_at"]

    def get_class_name(self, obj):
        return f"Grade {obj.class_obj.grade}"

    def get_section_name(self, obj):
        return obj.section.name if obj.section else None

    def get_school_name(self, obj):
        return obj.class_obj.school.name

    def validate(self, data):
        class_obj = data.get("class_obj")
        section = data.get("section")

        if section and section.class_obj != class_obj:
            raise serializers.ValidationError({
                "section": "Section does not belong to the same class as the selected class."
            })
        return data

    def create(self, validated_data):
        return Subject.objects.create(**validated_data)
