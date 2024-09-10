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

    path('exchange/', exchange, name='exchange'),
    path('api/crypto-data/', views.get_crypto_data_api, name='crypto_data_api'),

    path('crypto/chart/', views.crypto_chart_view, name='crypto_chart'),
    path('crypto/prices/', views.get_crypto_prices, name='get_crypto_prices'),

    path('create_wallet/', create_wallet, name='create_wallet'),
    path('wallet/<str:wallet_id>/', wallet_detail, name='wallet_detail'),
    path('wallets/', list_wallets, name='list_wallets'),
]
