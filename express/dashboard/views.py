from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from .models import UserForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        if UserForm.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        user = UserForm(username=username, email=email, phone_number=phone_number, password=password1)
        user.save()

        # Log the user in and save email in session
        user = authenticate(email=email, password=password1)
        if user is not None:
            auth_login(request, user)
            request.session['user_email'] = email

        return JsonResponse({'message': 'Sign Up successful'})
    return render(request, 'base/base.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserForm.objects.get(email=email)
        except UserForm.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return redirect('home')  # Redirect back to the home page if login fails

        # Check if the provided password matches the stored hashed password
        if check_password(password, user.password):
            request.session['email'] = user.email  # Save the user's email in the session
            return redirect('home')  # Redirect to the 'about' page on successful login
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('home')  # Redirect back to the home page if login fails

    return render(request, 'base/base.html')  # Render the login modal within the base template
def logout_user(request):
    auth_logout(request)
    request.session.flush()  # Clear session data
    return redirect('home')
# Create your views here.
def home(request):
    return render(request, 'home/index.html')


def about(request):
    return render(request, 'home/about.html')


def service(request):
    return render(request, 'home/service.html')

def road_map(request):
    return render(request, 'home/road_map.html')

def contact_us(request):
    return render(request, 'home/contact_us.html')
