from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage
import random
import string
from .forms import *
from .models import Registration,Courses
from django.conf import settings

def homepage(request):

    return render(request, 'index.html')

def generate_secret_code():
    """
    Generate a unique 5-letter secret code.
    
    Returns:
        str: A unique 5-character code consisting of uppercase letters and digits
    """
    while True:
        # Generate a 5-character code using uppercase letters and digits
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        # Check if this code already exists in the database
        if not Registration.objects.filter(secret_code=code).exists():
            return code





def prospectus(request):
    all_courses = Courses.objects.all()
    if request.method == 'POST':
        # Create form instance with POST data
        form = RegistrationForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            try:
                # Save the registration without committing to the database
                registration = form.save(commit=False)
                
                # Generate and set the secret code
                registration.secret_code = generate_secret_code()
                
                # Save the registration to the database
                registration.save()
                
                # Store the registration ID in the session
                request.session['registration_id'] = registration.id

                # Redirect to the success page
                return redirect('success')
            except Exception as e:

                messages.error(request, f"Registration failed: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = RegistrationForm()
        
        
    
    # Render the prospectus page with the form
    return render(request, 'propestus.html', {'form': form, 'all_courses': all_courses})



def success(request):
    all_courses = Courses.objects.all()

    # Get the registration ID from the session
    registration_id = request.session.get('registration_id')

    if not registration_id:
        # If no ID is found in the session, show an error message
        return render(request, 'registration-success.html', {
            'error': 'No registration found for this session.'
        })

    try:
        # Retrieve the specific registration record
        registration = Registration.objects.get(id=registration_id)
        course = registration.course
        
        # # Clear the session ID to prevent duplicate access
        # del request.session['registration_id']

        # Render the success page with registration details
        return render(request, 'registration-success.html', {
            'secret_code': registration.secret_code,
            'first_name': registration.first_name,
            'last_name': registration.last_name,
            'email': registration.email,
            'age': registration.age,
            'address': registration.address,
            'course_price': course.price,
            'education_level': registration.get_education_level_display(),
            'teaching_method': registration.get_teaching_method_display(),
            'currently_in_school': registration.get_currently_in_school_display(),
            'all_courses': all_courses
        })
    except Registration.DoesNotExist:
        return render(request, 'registration-success.html', {
            'error': 'Registration not found.'
        })




import logging
logger = logging.getLogger(__name__)

def proof(request):
    """
    Handle proof submission and send the uploaded file via email.
    """
    if request.method == 'POST':
        form = ProofForm(request.POST, request.FILES)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            passcode = form.cleaned_data['passcode']
            proof_file = request.FILES['proof_file']
            
            # Prepare email details
            email_subject = "Proof of Payment Submission"
            email_body = f"Payment proof submitted by:\n\nName: {full_name}\nPasscode: {passcode}"
            recipient_email = "chrispadiga@gmail.com"  # Change this to your desired recipient email
            
            try:
                email = EmailMessage(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,  # Use EMAIL_HOST_USER instead of DEFAULT_FROM_EMAIL
                    [recipient_email]
                )
                
                # Attach the uploaded file
                email.attach(proof_file.name, proof_file.read(), proof_file.content_type)
                
                # Send the email
                email.send()
                return render(request, 'proof_success.html', {
                    'message': 'Your proof has been submitted successfully!',
                })
            except Exception as e:
                # More detailed logging
                logger.error(f"Email sending failed: {str(e)}")
                return render(request, 'send_proof.html', {
                    'form': form,
                    'error': f"Failed to send proof: {str(e)}"
                })
    else:
        form = ProofForm()
    
    return render(request, 'send_proof.html', {'form': form})




# from django.core.mail import send_mail

# # Email variables
# email_sender = 'Padigachris@gmail.com'
# email_receiver = 'Chrispadiga@gmail.com'
# subject = 'Dont forget to reach me today x'
# body = 'Dont forget to subscribe'

# # Send email
# send_mail(
#     subject,
#     body,
#     email_sender,  # From email
#     [email_receiver],  # To email
#     fail_silently=False,
# )

# print('Message sent')
