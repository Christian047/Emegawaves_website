from django.db import models
import random
import string

class Registration(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=False, null=True, blank=True)
    age = models.IntegerField()
    address = models.CharField(max_length=255)
    
    COURSE_CHOICES = [
        ('computer_appreciation', 'Computer Appreciation'),
        ('microsoft_word', 'Microsoft Word'),
        ('microsoft_excel', 'Microsoft Excel'),
        ('microsoft_access', 'Microsoft Access'),
        ('microsoft_powerpoint', 'Microsoft Powerpoint'),
    ]
    
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
    
    course = models.CharField(max_length=50, choices=COURSE_CHOICES)
    education_level = models.CharField(max_length=50, choices=EDUCATION_CHOICES)
    teaching_method = models.CharField(max_length=50, choices=TEACHING_METHOD_CHOICES)
    currently_in_school = models.CharField(max_length=50, choices=SCHOOL_STATUS_CHOICES)
    
    # Remove the default generator, we'll generate it in the view
    secret_code = models.CharField(max_length=5, unique=True, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"