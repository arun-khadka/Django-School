from django.db import models
from school.models import School
from django.utils import timezone

class ExamTerm(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="exam_terms",  # unique name for reverse lookup
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("school", "name")

    def __str__(self):
        return f"{self.name} ({self.school.name})"
