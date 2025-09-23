from django.db import models
from classes.models import Class
from section.models import Section


class Subject(models.Model):
    name = models.CharField(max_length=255)
    class_obj = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="subjects"
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="subjects",
        null=True,
        blank=True,  # allow subjects without section
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.section:
            return f"{self.name} - Grade {self.class_obj.grade} - {self.section.name}"
        return f"{self.name} - Grade {self.class_obj.grade}"
