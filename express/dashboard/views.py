from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from .models import *
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
import requests
from django.conf import settings
from .decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from web3 import Web3
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

    return render(request, 'wallet/wallet.html')


@login_required
@csrf_exempt
def save_wallet_address(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            wallet_address = data.get('wallet_address')

            if wallet_address:
                # Get or create the Wallet object for the logged-in user
                wallet, created = Wallet.objects.get_or_create(user=request.user)

                # Update the wallet address
                wallet.wallet_address = wallet_address
                wallet.save()

                return JsonResponse({'success': True, 'message': 'Wallet address saved successfully!'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid wallet address.'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



@login_required
def save_wallet_address(request):
    if request.method == "POST":
        try:
            # Load wallet address from request body
            data = json.loads(request.body)
            wallet_address = data.get('wallet_address')

            if not wallet_address:
                return JsonResponse({'status': 'error', 'message': 'No wallet address provided'}, status=400)

            # Fetch the logged-in user's email from session and find corresponding UserForm
            user_email = request.session.get('email')
            user = get_object_or_404(UserForm, email=user_email)

            # Check if user already has a wallet
            wallet, created = Wallet.objects.get_or_create(user=user)

            # Update the wallet address and save
            wallet.wallet_address = wallet_address
            wallet.save()

            return JsonResponse({'status': 'success', 'message': 'Wallet address saved successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def wallet_detail(request, wallet_address):
    # Optionally, you could retrieve the wallet from the database using the wallet_address
    # For example:
    # wallet = Wallet.objects.filter(wallet_address=wallet_address).first()

    context = {
        'wallet_address': wallet_address,  # Send the wallet address to the template
    }
    return render(request, 'wallet/metamask.html', context)


@login_required
def disconnect_wallet(request):
    if request.method == 'POST':
        try:
            # Get the user's email from the session
            user_email = request.session.get('email')
            user = UserForm.objects.get(email=user_email)

            # Find the user's wallet and clear the wallet address
            wallet = Wallet.objects.filter(user=user).first()
            if wallet:
                wallet.wallet_address = None  # Clear wallet address
                wallet.save()

            # Optionally, you can also clear session data if required
            # del request.session['wallet_address']  # Clear session wallet info if needed

            return JsonResponse({'status': 'success', 'message': 'Wallet disconnected successfully'})
        except UserForm.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
@login_required
def save_transaction(request):
    if request.method == 'POST':
        try:
            # Load JSON data from the request
            data = json.loads(request.body)

            # Get the user based on the email stored in session
            user_email = request.session.get('email')
            user = get_object_or_404(UserForm, email=user_email)

            # Save the transaction details in the Transaction model
            transaction = Transaction(
                user=user,
                recipient_address=data['recipient_address'],
                amount=data['amount'],
                status=data['status'],
                transaction_hash=data['transaction_hash'],
                reason=data.get('reason', '')  # Optional field
            )
            transaction.save()

            # Return a success response
            return JsonResponse({'status': 'success'}, status=201)
        
        except Exception as e:
            # Handle any errors that occur and return an error response
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    # Return error if request method is not POST
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def transaction_history(request):
    # Get the user's email from the session
    user_email = request.session.get('email')

    # Check if the session email exists
    if not user_email:
        print("No email in session")
        return redirect('login')

    # Fetch the user and their transactions
    user = get_object_or_404(UserForm, email=user_email)
    transactions = Transaction.objects.filter(user=user).order_by('-created_at')
    # Render the transactions in the template
    return render(request, 'wallet/metamask.html', {'transactions': transactions})