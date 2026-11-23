
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator


class Profile(models.Model):

    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('ADMIN', 'Admin'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='STUDENT'
    )

    contact_number = models.CharField(
        max_length=20,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class ActivityRecord(models.Model):

    ACTIVITY_CHOICES = [
        ('PRODUCTIVE', 'Productive'),
        ('DISTRACTING', 'Distracting'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activity_records'
    )

    activity_name = models.CharField(
        max_length=150
    )

    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_CHOICES
    )

    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    recorded_at = models.DateTimeField(
        default=timezone.now
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.activity_name} - {self.user.username}"
