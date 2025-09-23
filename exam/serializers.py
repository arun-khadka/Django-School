from rest_framework import serializers
from section.models import Section
from classes.models import Class
from school.models import School
from .models import ExamTerm


class ExamTermSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source="school.name", read_only=True)

    class Meta:
        model = ExamTerm
        fields = ["id", "school", "name", "school_name", "created_at"]
        read_only_fields = ["id", "school_name", "created_at"]

class MarksheetImportSerializer(serializers.Serializer):
    file = serializers.FileField()
    full_mark = serializers.FloatField(default=100)
    pass_mark = serializers.FloatField(default=33)
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    class_obj = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    section = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.all(), allow_null=True
    )
    term = serializers.PrimaryKeyRelatedField(queryset=ExamTerm.objects.all())

    def validate(self, data):
        school = data.get("school")
        class_obj = data.get("class_obj")
        section = data.get("section")
        term = data.get("term")

        if class_obj.school != school:
            raise serializers.ValidationError(
                "Class does not belong to the specified school."
            )
        if term.school != school:
            raise serializers.ValidationError(
                "Term does not belong to the specified school."
            )
        if section and (section.school != school or section.class_obj != class_obj):
            raise serializers.ValidationError(
                "Section does not belong to the specified school or class."
            )
        return data
