# urls.py
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .views import *
urlpatterns = [

    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),

    path('', home, name='home'),
    path('about/', about, name='about'),
    path('service/', service, name='service'),
    path('road map/', road_map, name='road_map'),
    path('contact us/', contact_us, name='contact_us'),
]