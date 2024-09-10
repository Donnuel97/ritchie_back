from http.client import HTTPException
from django.conf import settings

from django_bitgo.client import BitGoClient
from django_bitgo.exceptions import BitGoException


class Address:
    def __init__(self, client, wallet_id) -> None:
        self.client = client or BitGoClient()
        self.wallet_id = wallet_id or settings.BITGO_WALLET_ID

    def list_addresses(self, coin: str = "tbtc", wallet_id: str = ""):
        try:
            response = self.client.request(
                method="GET", path=f"{coin}/wallet/{wallet_id}/addresses"
            )
        except HTTPException:
            raise HTTPException("A connection error raised! Please check again later.")
        except Exception as e:
            raise Exception(f"Generic exception raised, {str(e)}")
        return response.json()

    def create_address(
        self, coin: str = "tbtc", wallet_id: str = "", payload: dict = {}
    ):
        try:
            response = self.client.request(
                method="POST",
                path=f"{coin}/wallet/{wallet_id}/address",
                payload=payload,
            )
        except HTTPException:
            raise HTTPException("A connection error raised! Please check again later.")
        except Exception as e:
            raise Exception(f"Generic exception raised, {str(e)}")
        return response.json()

    def deploy_address(
        self,
        address_id: str,
        coin: str = "tbtc",
        wallet_id: str = "",
        payload: dict = {},
    ):
        if not address_id:
            raise BitGoException("Address id is missing but required.")

        try:
            response = self.client.request(
                method="POST",
                path=f"{coin}/wallet/{wallet_id}/address/{address_id}/deployment",
                payload=payload,
            )
        except HTTPException:
            raise HTTPException("A connection error raised! Please check again later.")
        except Exception as e:
            raise Exception(f"Generic exception raised, {str(e)}")
        return response.json()

    def get_address(self, address_id: str, coin: str = "tbtc", wallet_id: str = ""):
        if not address_id:
            raise BitGoException("Address id is missing but required.")

        try:
            response = self.client.request(
                method="GET",
                path=f"{coin}/wallet/{wallet_id}/address/{address_id}",
            )
        except HTTPException:
            raise HTTPException("A connection error raised! Please check again later.")
        except Exception as e:
            raise Exception(f"Generic exception raised, {str(e)}")
        return response.json()
