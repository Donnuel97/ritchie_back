from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
import requests
from django.conf import settings
from .decorators import login_required
# from .utils import create_bitgo_wallet


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
            return redirect('login')  # Redirect to login page if email is not found

        # Check if the provided password matches the stored hashed password
        if check_password(password, user.password):
            # Store user information in session upon successful login
            request.session['email'] = user.email
            return redirect('home')  # Redirect to the home page on successful login
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')  # Redirect back to login page if password is incorrect

    return render(request, 'base/base.html')

def logout_user(request):
    auth_logout(request)
    request.session.flush()  # Clear session data
    return redirect('home')
# Create your views here.
def home(request):
    return render(request, 'home/index.html')

@login_required
def about(request):
    return render(request, 'home/about.html')


def service(request):
    return render(request, 'home/service.html')

def road_map(request):
    return render(request, 'home/road_map.html')

def contact_us(request):
    return render(request, 'home/contact_us.html')

def crypto_chart_view(request):
    # Render the page with the chart
    return render(request, 'home/chart.html')
def get_crypto_prices(request):
    # API endpoint to fetch live cryptocurrency prices
    api_key = settings.CRYPTOCOMPARE_API_KEY
    url = f"https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"

    headers = {
        'authorization': f'Apikey {api_key}'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return JsonResponse(data)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Error fetching data'}, status=500)




def exchange(request):
    api_key = settings.CRYPTOCOMPARE_API_KEY
    url = f"https://min-api.cryptocompare.com/data/top/mktcapfull?limit=10&tsym=USD"

    headers = {
        'authorization': f'Apikey {api_key}'
    }

    # Make the API request
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Extract relevant crypto data
        crypto_data = []
        for coin in data['Data']:
            crypto_data.append({
                'name': coin['CoinInfo']['FullName'],
                'symbol': coin['CoinInfo']['Name'],
                'price': coin['RAW']['USD']['PRICE'],
                'market_cap': coin['RAW']['USD']['MKTCAP'],
                'volume_24h': coin['RAW']['USD']['TOTALVOLUME24H'],
                'change_24h': coin['RAW']['USD']['CHANGEPCT24HOUR']
            })
    except requests.exceptions.RequestException as e:
        crypto_data = [{'error': 'Error fetching data from CryptoCompare.'}]

    return render(request, 'home/exchange.html', {'crypto_data': crypto_data})


def get_crypto_data_api(request):
    api_key = settings.CRYPTOCOMPARE_API_KEY
    url = "https://min-api.cryptocompare.com/data/top/mktcapfull?limit=10&tsym=USD"

    headers = {
        'authorization': f'Apikey {api_key}'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Extract relevant crypto data
        crypto_data = []
        for coin in data['Data']:
            crypto_data.append({
                'name': coin['CoinInfo']['FullName'],
                'symbol': coin['CoinInfo']['Name'],
                'price': coin['RAW']['USD']['PRICE'],
                'market_cap': coin['RAW']['USD']['MKTCAP'],
                'volume_24h': coin['RAW']['USD']['TOTALVOLUME24H'],
                'change_24h': coin['RAW']['USD']['CHANGEPCT24HOUR']
            })

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Error fetching data from CryptoCompare.'})

    return JsonResponse({'crypto_data': crypto_data})


@login_required
def create_wallet(request):
    user = UserForm.objects.get(email=request.session['email'])

    if request.method == 'POST':
        wallet_password = request.POST.get('wallet_password')

        if len(wallet_password) < settings.WALLET_PASSWORD_MIN_LENGTH:
            messages.error(request, 'Password too short.')
            return redirect('create_wallet')

        existing_wallet = Wallet.objects.filter(user=user, coin='btc').first()
        if existing_wallet:
            messages.error(request, 'You already have a Bitcoin wallet.')
            return redirect('wallet_detail', wallet_id=existing_wallet.wallet_id)

        url = f"{settings.BITGO_API_URL}/btc/wallet"

        headers = {
            'Authorization': f"Bearer {settings.BITGO_ACCESS_TOKEN}",
            'Content-Type': 'application/json',
        }
        payload = {
            "passphrase": wallet_password,
            "label": f"{user.username}_BTC_wallet"
        }

        response = requests.post(url, json=payload, headers=headers)

        # Print status code and raw response content for debugging
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)  # Use response.text to see raw response

        try:
            response_data = response.json()
            if response.status_code == 200:
                Wallet.objects.create(
                    user=user,
                    wallet_id=response_data['id'],
                    coin='btc',
                    label=response_data.get('label', f"{user.username}'s BTC Wallet"),
                    balance=0
                )
                messages.success(request, 'Bitcoin wallet created successfully.')
                return redirect('wallet_detail', wallet_id=response_data['id'])
            else:
                error_message = response_data.get('error', 'Error creating wallet.')
                messages.error(request, error_message)
        except ValueError:
            messages.error(request, 'Received non-JSON response from BitGo.')

        return redirect('create_wallet')
    return render(request, 'wallet/wallet.html')

# Wallet detail view
@login_required
def wallet_detail(request, wallet_id):
    user = UserForm.objects.get(email=request.session['email'])
    wallet = Wallet.objects.get(wallet_id=wallet_id, user=user)

    # Fetch wallet balance from BitGo
    url = f"{settings.BITGO_API_URL}/btc/wallet/{wallet.wallet_id}"
    headers = {
        'Authorization': f"Bearer {settings.BITGO_ACCESS_TOKEN}",
        'Content-Type': 'application/json',
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        wallet_data = response.json()
        wallet.balance = wallet_data['balance'] / 1e8  # Convert satoshis to BTC
        wallet.save()
        return render(request, 'wallet/detail.html', {'wallet': wallet})
    else:
        messages.error(request, 'Failed to retrieve wallet details.')
        return redirect('home')

# List all wallets
@login_required
def list_wallets(request):
    user = UserForm.objects.get(email=request.session['email'])
    wallets = Wallet.objects.filter(user=user)
    return render(request, 'wallet/success.html', {'wallets': wallets})
# def create_wallet_view(request):
#     if request.method == "POST":
#         coin = request.POST.get("coin", "btc")
#         label = request.POST.get("label", f"{request.session['email']}'s Wallet")
#
#         # Call the BitGo API to create the wallet
#         wallet_data = create_bitgo_wallet(user_email=request.session['email'], coin=coin, label=label)
#         if wallet_data:
#             try:
#                 # Fetch user using email from the session
#                 user = UserForm.objects.get(email=request.session['email'])
#
#                 # Save wallet information in the database
#                 Wallet.objects.create(
#                     user=user,
#                     wallet_id=wallet_data.get("id"),
#                     coin=coin,
#                     label=label,
#                     balance=0,  # Update balance later if needed
#                 )
#                 return redirect('wallet_success')
#             except UserForm.DoesNotExist:
#                 return render(request, "wallet/wallet.html", {"error": "User does not exist. Please log in again."})
#
#         return render(request, "wallet/wallet.html", {"error": "Failed to create wallet. Please try again."})
#
#     return render(request, "wallet/wallet.html")
def wallet_success(request):
    return render(request, "wallet/success.html")