from django.shortcuts import render, redirect
from .models import Payment, UserWallet
from django.conf import settings
from django.contrib import messages
from base.models import Registration


def initiate_payment(request):
    registration_id = request.session.get('registration_id')
    if not registration_id:
        messages.error(request, "Session expired. Please register again.")
        return redirect('prospectus')

    registration = Registration.objects.filter(id=registration_id).first()
    if not registration:
        messages.error(request, "Registration not found for this session.")
        return redirect('prospectus')

    # Retrieve the course associated with the registration
    course = registration.course

    if request.method == "POST":
        amount = request.POST['amount']
        email = request.POST['email']

        pk = settings.PAYSTACK_PUBLIC_KEY
        session_id = request.session.session_key

        try:
            # Create the payment record
            payment = Payment.objects.create(
                amount=amount,
                email=email,
                session_id=session_id,
                registration=registration  # Associate payment with registration
            )
            payment.save()
        except Exception as e:
            messages.error(request, f"An error occurred while creating the payment: {str(e)}")
            return redirect('initiate_payment')

        context = {
            'payment': payment,
            'field_values': request.POST,
            'paystack_pub_key': pk,
            'amount_value': payment.amount_value(),
            'course_price': course.price,
            'course_name': course.name,
          
            
        }
        return render(request, 'make_payment.html', context)

    # Render the payment page for GET requests
    return render(request, 'payment.html', {'course_price': course.price, 'course_name': course.name})

def verify_payment(request, ref):
	payment = Payment.objects.get(ref=ref)
	verified = payment.verify_payment()

	if verified:
		user_wallet = UserWallet.objects.get(user=request.user)
		user_wallet.balance += payment.amount
		user_wallet.save()
		print(request.user.username, " funded wallet successfully")
		return render(request, "success.html")
	return render(request, "success.html")



def verify_payment(request, ref):
    session_id = request.session.session_key

    try:
        payment = Payment.objects.get(ref=ref, session_id=session_id)
    except Payment.DoesNotExist:
        messages.error(request, "Payment not found or does not match this session.")
        return render(request, "payments/failure.html")

    verified = payment.verify_payment()

    if verified:
            # Payment was successful
            messages.success(request, "Payment successful, registration complete.")
            return render(request, "success.html", {'message': "Payment verified successfully!"})
    
    return render(request, "failure.html", {'message': "Payment verification failed."})


# Geting The session from the main views

# def prospectus(request):
#     all_courses = Courses.objects.all()
#     if request.method == 'POST':
#         # Create form instance with POST data
#         form = RegistrationForm(request.POST)
#         # Check if the form is valid
#         if form.is_valid():
#             try:
#                 # Save the registration without committing to the database
#                 registration = form.save(commit=False)
                
#                 # Generate and set the secret code
#                 registration.secret_code = generate_secret_code()
                
#                 # Save the registration to the database
#                 registration.save()
                
#                 # Store the registration ID in the session
#                 request.session['registration_id'] = registration.id

#                 # Redirect to the success page
#                 return redirect('success')
#             except Exception as e:

#                 messages.error(request, f"Registration failed: {str(e)}")
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{field.capitalize()}: {error}")
#     else:
#         form = RegistrationForm()
        
        
    
#     # Render the prospectus page with the form
#     return render(request, 'propestus.html', {'form': form, 'all_courses': all_courses})




