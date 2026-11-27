
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        STAFF = 'STAFF', 'Staff'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT
    )

    course = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username


class StudentProfile(models.Model):
    student_id = models.AutoField(primary_key=True)

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    institutional_id = models.CharField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.user.username


class StaffProfile(models.Model):
    staff_id = models.AutoField(primary_key=True)

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='staff_profile'
    )

    institutional_id = models.CharField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.user.username
