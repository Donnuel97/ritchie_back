# urls.py
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('sign-up/', sign_up, name='sign_up'),
    path('login/', views.login_user, name='login'),
    path('logout/', logout_user, name='logout_user'),

    path('', home, name='home'),
    path('about/', about, name='about'),
    path('service/', service, name='service'),
    path('road map/', road_map, name='road_map'),
    path('contact us/', contact_us, name='contact_us'),
]