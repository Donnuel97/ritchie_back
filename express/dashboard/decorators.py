from django.shortcuts import redirect
from django.urls import reverse

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'email' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper