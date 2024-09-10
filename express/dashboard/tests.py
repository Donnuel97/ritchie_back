from django.test import TestCase
# tests.py or a standalone script
from bitgo import BitGo
from django.conf import settings

def test_bitgo_wallet_creation():
    bitgo = BitGo(access_token=settings.BITGO_ACCESS_TOKEN)
    try:
        wallet = bitgo.wallets.create_wallet(
            coin='btc',
            label='Test Wallet',
            passphrase='your-secure-passphrase'
        )
        print(wallet.to_dict())
    except Exception as e:
        print(f"Error creating wallet: {e}")

test_bitgo_wallet_creation()

# Create your tests here.
