from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'age', 
            'address', 
            'course', 
            'education_level', 
            'teaching_method', 
            'currently_in_school'
        ]
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if email already exists
        if Registration.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and (age < 5 or age > 100):
            raise forms.ValidationError("Please enter a valid age between 5 and 100.")
        return age
    
    
class ProofForm(forms.Form):
        full_name = forms.CharField(max_length=255, label="Full Name")
        passcode = forms.CharField(max_length=50, label="Passcode")
        proof_file = forms.FileField(label="Payment Slip")
