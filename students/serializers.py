from rest_framework import serializers
from students.models import Student, StudentMarks, StudentSubjectMarks
from school.models import School
from classes.models import Class
from section.models import Section
from exam.models import ExamTerm
from subject.models import Subject


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


class StudentSubjectMarksSerializer(serializers.ModelSerializer):
    subject_name = serializers.ReadOnlyField(source="subject.name")
    student_name = serializers.ReadOnlyField(source="student_marks.student.name")

    class Meta:
        model = StudentSubjectMarks
        fields = [
            "id",
            "student_marks",
            "student_name",
            "subject",
            "subject_name",
            "marks_obtained",
        ]


class StudentMarksSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source="student.name")
    subject_marks = StudentSubjectMarksSerializer(many=True, read_only=True)

    class Meta:
        model = StudentMarks
        fields = [
            "id",
            "student",
            "student_name",
            "total_marks",
            "percentage",
            "grade",
            "result",
            "rank",
            "subject_marks",
            "created_at",
            "updated_at",
        ]


class StudentSerializer(serializers.ModelSerializer):
    school_name = serializers.ReadOnlyField(source="school.name")
    class_grade = serializers.ReadOnlyField(source="class_obj.grade")
    section_name = serializers.ReadOnlyField(source="section.name")
    term_name = serializers.ReadOnlyField(source="term.name")
    marks = StudentMarksSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "school",
            "school_name",
            "class_obj",
            "class_grade",
            "section",
            "section_name",
            "term",
            "term_name",
            "name",
            "roll_no",
            "otp",
            "marks",
            "created_at",
            "updated_at",
        ]
