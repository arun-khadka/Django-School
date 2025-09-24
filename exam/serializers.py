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
    full_mark = serializers.FloatField(default=100)
    pass_mark = serializers.FloatField(default=33)
    file = serializers.FileField()
    
    
