# # utils.py
# import bitgo
# from django.conf import settings
#
# def create_bitgo_wallet(user_email, coin="btc", label="My Wallet"):
#     # Initialize the BitGo client
#     bitgo = BitGo(access_token=settings.BITGO_ACCESS_TOKEN)
#
#     try:
#         # Create the wallet
#         wallet = bitgo.wallets.create_wallet(
#             coin=coin,
#             label=label,
#             passphrase="your-secure-passphrase"  # Ensure you use a secure passphrase
#         )
#         return wallet.to_dict()  # Convert wallet object to dictionary
#     except Exception as e:
#         # Log the error for debugging
#         print(f"Error creating wallet: {e}")
#         return None
#
#
# # # utils.py
# # import requests
# # from django.conf import settings
# #
# # def create_bitgo_wallet(user_email, coin="btc", label="My Wallet"):
# #     url = f"{settings.BITGO_API_URL}/{coin}/wallet"  # Ensure URL is correct
# #     headers = {
# #         "Authorization": f"Bearer {settings.BITGO_ACCESS_TOKEN}",
# #         "Content-Type": "application/json",
# #     }
# #     data = {
# #         "label": label,
# #         "passphrase": "your-secure-passphrase",  # Replace with a secure passphrase
# #         "enterprise": None,  # Optional: For enterprise accounts
# #     }
# #
# #     response = requests.post(url, json=data, headers=headers)
# #     if response.status_code == 200:
# #         wallet_data = response.json()
# #         return wallet_data
# #     else:
# #         # Log the error for debugging
# #         print(f"Error: {response.status_code} - {response.text}")
# #         return None

import requests

BLOCKCYPHER_BASE_URL = "https://api.blockcypher.com/v1"
API_TOKEN = "22b517213c354b52bd2119f038aeb970"  # Replace with your BlockCypher API token


def create_wallet(coin="btc"):
    url = f"{BLOCKCYPHER_BASE_URL}/{coin}/main/addrs"

    # Send POST request to create a new wallet
    response = requests.post(url, params={"token": API_TOKEN})

    if response.status_code == 201:
        return response.json()  # Contains wallet info like address and private key
    else:
        raise Exception(f"Error creating wallet: {response.text}")
