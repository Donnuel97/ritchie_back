from django_bitgo.client import BitGoClient
import pytest


def test_address_initialize_module_without_access_token():

    with pytest.raises(BitGoClient) as exc:
        BitGoClient()

    assert str(exc.value) == "Access token is required to create a BitGoClient"
