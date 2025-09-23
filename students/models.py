from django.db import models
from django.utils import timezone

from classes.models import Class as ClassModel
from section.models import Section
from subject.models import Subject
from exam.models import ExamTerm
from school.models import School
from exam.models import ExamTerm  


class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="students")
    class_obj = models.ForeignKey(ClassModel, on_delete=models.CASCADE, related_name="students")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="students")
    term = models.ForeignKey(ExamTerm, on_delete=models.CASCADE, related_name="students", null=True)  # new field
    name = models.CharField(max_length=255)
    roll_no = models.IntegerField()
    otp = models.CharField(max_length=50, blank=True)  # admin fills manually in Excel
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # track updates automatically

    class Meta:
        ordering = ['class_obj', 'section', 'roll_no']

    def __str__(self):
        return f"{self.name} (Roll {self.roll_no})"


class StudentMarks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="marks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    total_marks = models.FloatField(blank=True, null=True)
    percentage = models.FloatField(blank=True, null=True)
    grade = models.CharField(max_length=5, blank=True, null=True)
    result = models.CharField(max_length=10, choices=[("Pass", "Pass"), ("Fail", "Fail")], blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.name} Marks"

class StudentSubjectMarks(models.Model):
    student_marks = models.ForeignKey(StudentMarks, on_delete=models.CASCADE, related_name="subject_marks")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()

    class Meta:
        unique_together = ("student_marks", "subject")

    def __str__(self):
        return f"{self.subject.name} - {self.marks_obtained}"