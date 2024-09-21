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
    path('save-wallet-address/', views.save_wallet_address, name='save_wallet_address'),
    path('disconnect_wallet/', views.disconnect_wallet, name='disconnect_wallet'),  # URL for disconnecting
    path('wallet/<str:wallet_address>/', views.wallet_detail, name='wallet_detail'),  # New URL for the wallet detail page
    path('save_transaction/', save_transaction, name='save_transaction'),
    path('transaction-history/', transaction_history, name='transaction_history'),
]
