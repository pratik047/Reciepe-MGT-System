from collections.abc import Iterable
from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet

User = get_user_model()


class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_delete=True)


class Receipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    receipe_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    receipe_description = models.TextField()
    receipe_image = models.ImageField(upload_to="receipe")
    receipe_view_count = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.receipe_name)
        return super(Receipe, self).save(*args, **kwargs)


class Department(models.Model):
    department = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.department

    class Meta:
        ordering = ["department"]


class StudentID(models.Model):
    student_id = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.student_id


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.subject_name


class Student(models.Model):
    department = models.ForeignKey(
        Department, related_name="depart", on_delete=models.CASCADE
    )
    student_id = models.OneToOneField(
        StudentID, related_name="student_profile", on_delete=models.CASCADE
    )
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    student_age = models.IntegerField(default=18)
    student_address = models.CharField(max_length=255)
    is_delete = models.BooleanField(default=False)

    objects = models.Manager()
    admin_objects = StudentManager()

    def __str__(self):
        return self.student_name

    class Meta:
        ordering = ["student_name"]
        verbose_name = "student"


class SubjectMarks(models.Model):
    student = models.ForeignKey(
        Student, related_name="studentmarks", on_delete=models.CASCADE
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.student.student_name} {self.subject.subject_name}"

    class Meta:
        unique_together = ["student", "subject"]


class Reportcard(models.Model):
    student = models.ForeignKey(
        Student, related_name="studentreportcard", on_delete=models.CASCADE
    )
    student_rank = models.IntegerField()
    date_of_report_card_generation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["student_rank", "date_of_report_card_generation"]
