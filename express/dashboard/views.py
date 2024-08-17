from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .forms import CustomUserCreationForm, CustomAuthenticationForm


# Create your views here.

class SignUpView(View):
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'success': 'Registration successful.'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(self.request, username=email, password=password)
            if user is not None:
                login(self.request, user)
                return JsonResponse({'success': 'Login successful.'})
            else:
                return JsonResponse({'errors': 'Invalid email or password.'}, status=400)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)

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
