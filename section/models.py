from django.db import models
from school.models import School
from classes.models import Class


class Section(models.Model):
    name = models.CharField(max_length=255)
    class_obj = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="sections",
        null=True,
        blank=True, 
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="sections",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("name", "class_obj") 

    def __str__(self):
        return f"{self.name} - {self.class_obj.name} ({self.class_obj.school.name})"

