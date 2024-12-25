from django.db import models
from django.core.validators import MinValueValidator

class Courses(models.Model):
    name = models.CharField(max_length=50)  # Made required
    price = models.IntegerField(validators=[MinValueValidator(0)])  # Added validator

    def __str__(self):
        return self.name

class Registration(models.Model):
    EDUCATION_CHOICES = [
        ('primary', 'Primary'),
        ('secondary', 'Secondary School'),
        ('university', 'University'),
    ]

    TEACHING_METHOD_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    SCHOOL_STATUS_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    age = models.IntegerField(validators=[MinValueValidator(0)])
    address = models.CharField(max_length=255)

    course = models.ForeignKey(Courses, related_name='registrations', on_delete=models.CASCADE)
    education_level = models.CharField(max_length=50, choices=EDUCATION_CHOICES)
    teaching_method = models.CharField(max_length=50, choices=TEACHING_METHOD_CHOICES)
    currently_in_school = models.CharField(max_length=50, choices=SCHOOL_STATUS_CHOICES)

    secret_code = models.CharField(max_length=5, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"