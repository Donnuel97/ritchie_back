from .forms import SignUpForm, LoginForm

def add_forms_to_context(request):
    return {
        'signup_form': SignUpForm(),
        'login_form': LoginForm(),
    }
