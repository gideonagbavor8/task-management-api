from django.db import models
from django.contrib.auth.models import User  # Use Django's built-in User model
from django.core.exceptions import ValidationError
from django.utils.timezone import now


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')  # Link categories to users

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')  # Link tasks to users
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    priority_level = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    completed_timestamp = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name='tasks', null=True, blank=True)

    # Custom clean method for due_date validation
    def clean(self):
        if self.due_date < now():
            raise ValidationError("Due date cannot be in the past.")

    def __str__(self):
        return self.title
