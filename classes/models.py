from django.db import models
from school.models import School

class Class(models.Model):
    GRADE_CHOICES = [(i, str(i)) for i in range(1, 11)]  # Grades 1 to 10
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="classes")
    grade = models.IntegerField(choices=GRADE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("school", "grade")  # Each grade unique per school
        ordering = ["grade"]

    def __str__(self):
        return f"Grade {self.grade} ({self.school.name})"

    @property
    def has_sections(self):
        # Returns True if this class has any sections
        return self.sections.exists() if hasattr(self, "sections") else False
