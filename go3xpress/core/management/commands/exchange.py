from decimal import Decimal

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

# from requests_html import HTMLSession
from darkcodr.utils.logger import LOGGER
from darkcodr.core.models import Currency


class Command(BaseCommand):
    """
    This just retrieves a set of currency current prices respective to USD
    """

    help = _("Collect current bank rates")

    def handle(self, *args, **kwargs):
        Currency.objects.update_or_create(code="USD", defaults={"symbol": "USD", "price": Decimal(1)})

        url = str(settings.URL)

        ng = {"format": "json", "from": "USD", "to": "NGN", "amount": "1"}
        eu = {"format": "json", "from": "USD", "to": "EUR", "amount": "1"}
        gb = {"format": "json", "from": "USD", "to": "GBP", "amount": "1"}
        cn = {"format": "json", "from": "USD", "to": "CNY", "amount": "1"}
        jp = {"format": "json", "from": "USD", "to": "JPY", "amount": "1"}
        au = {"format": "json", "from": "USD", "to": "AUD", "amount": "1"}
        ca = {"format": "json", "from": "USD", "to": "CAD", "amount": "1"}
        ch = {"format": "json", "from": "USD", "to": "CHF", "amount": "1"}
        dk = {"format": "json", "from": "USD", "to": "DKK", "amount": "1"}
        se = {"format": "json", "from": "USD", "to": "SEK", "amount": "1"}
        za = {"format": "json", "from": "USD", "to": "ZAR", "amount": "1"}
        ae = {"format": "json", "from": "USD", "to": "AED", "amount": "1"}

        headers = {
            'x-rapidapi-host': "currency-converter5.p.rapidapi.com",
            'x-rapidapi-key': str(settings.API)
        }

        ng_res = requests.request("GET", url, headers=headers, params=ng)
        eu_res = requests.request("GET", url, headers=headers, params=eu)
        gb_res = requests.request("GET", url, headers=headers, params=gb)
        cn_res = requests.request("GET", url, headers=headers, params=cn)
        jp_res = requests.request("GET", url, headers=headers, params=jp)
        au_res = requests.request("GET", url, headers=headers, params=au)
        ca_res = requests.request("GET", url, headers=headers, params=ca)
        ch_res = requests.request("GET", url, headers=headers, params=ch)
        dk_res = requests.request("GET", url, headers=headers, params=dk)
        se_res = requests.request("GET", url, headers=headers, params=se)
        za_res = requests.request("GET", url, headers=headers, params=za)
        ae_res = requests.request("GET", url, headers=headers, params=ae)

        if ng_res.status_code == 200:
            ng_data = ng_res.json()
            ng_rate = ng_data["rates"]["NGN"]["rate"]
            Currency.objects.update_or_create(code="NGN", defaults={"symbol": "₦", "price": Decimal(ng_rate)})
            LOGGER.info(f"NGN rate updated to {ng_rate}")
        else:
            LOGGER.error(f"NGN rate not updated")

        if eu_res.status_code == 200:
            eu_data = eu_res.json()
            eu_rate = eu_data["rates"]["EUR"]["rate"]
            Currency.objects.update_or_create(code="EUR", defaults={"symbol": "€", "price": Decimal(eu_rate)})
            LOGGER.info(f"EUR rate updated to {eu_rate}")
        else:
            LOGGER.error(f"EUR rate not updated")

        if gb_res.status_code == 200:
            gb_data = gb_res.json()
            gb_rate = gb_data["rates"]["GBP"]["rate"]
            Currency.objects.update_or_create(code="GBP", defaults={"symbol": "£", "price": Decimal(gb_rate)})
            LOGGER.info(f"GBP rate updated to {gb_rate}")
        else:
            LOGGER.error(f"GBP rate not updated")

        if cn_res.status_code == 200:
            cn_data = cn_res.json()
            cn_rate = cn_data["rates"]["CNY"]["rate"]
            Currency.objects.update_or_create(code="CNY", defaults={"symbol": "¥", "price": Decimal(cn_rate)})
            LOGGER.info(f"CNY rate updated to {cn_rate}")
        else:
            LOGGER.error(f"CNY rate not updated")

        if jp_res.status_code == 200:
            jp_data = jp_res.json()
            jp_rate = jp_data["rates"]["JPY"]["rate"]
            Currency.objects.update_or_create(code="JPY", defaults={"symbol": "¥", "price": Decimal(jp_rate)})
            LOGGER.info(f"JPY rate updated to {jp_rate}")
        else:
            LOGGER.error(f"JPY rate not updated")

        if au_res.status_code == 200:
            au_data = au_res.json()
            au_rate = au_data["rates"]["AUD"]["rate"]
            Currency.objects.update_or_create(code="AUD", defaults={"symbol": "$", "price": Decimal(au_rate)})
            LOGGER.info(f"AUD rate updated to {au_rate}")
        else:
            LOGGER.error("AUD rate not updated")

        if ca_res.status_code == 200:
            ca_data = ca_res.json()
            ca_rate = ca_data["rates"]["CAD"]["rate"]
            Currency.objects.update_or_create(code="CAD", defaults={"symbol": "$", "price": Decimal(ca_rate)})
            LOGGER.info(f"CAD rate updated to {ca_rate}")
        else:
            LOGGER.error("CAD rate not updated")

        if ch_res.status_code == 200:
            ch_data = ch_res.json()
            ch_rate = ch_data["rates"]["CHF"]["rate"]
            Currency.objects.update_or_create(code="CHF", defaults={"symbol": "CHF", "price": Decimal(ch_rate)})
            LOGGER.info(f"CHF rate updated to {ch_rate}")
        else:
            LOGGER.error("CHF rate not updated")

        if dk_res.status_code == 200:
            dk_data = dk_res.json()
            dk_rate = dk_data["rates"]["DKK"]["rate"]
            Currency.objects.update_or_create(code="DKK", defaults={"symbol": "kr", "price": Decimal(dk_rate)})
            LOGGER.info(f"DKK rate updated to {dk_rate}")
        else:
            LOGGER.error("DKK rate not updated")

        if se_res.status_code == 200:
            se_data = se_res.json()
            se_rate = se_data["rates"]["SEK"]["rate"]
            Currency.objects.update_or_create(code="SEK", defaults={"symbol": "kr", "price": Decimal(se_rate)})
            LOGGER.info(f"SEK rate updated to {se_rate}")
        else:
            LOGGER.error("SEK rate not updated")

        if za_res.status_code == 200:
            za_data = za_res.json()
            za_rate = za_data["rates"]["ZAR"]["rate"]
            Currency.objects.update_or_create(code="ZAR", defaults={"symbol": "R", "price": Decimal(za_rate)})
            LOGGER.info(f"ZAR rate updated to {za_rate}")
        else:
            LOGGER.error("ZAR rate not updated")

        if ae_res.status_code == 200:
            ae_data = ae_res.json()
            ae_rate = ae_data["rates"]["AED"]["rate"]
            Currency.objects.update_or_create(code="AED", defaults={"symbol": "د.إ", "price": Decimal(ae_rate)})
            LOGGER.info(f"AED rate updated to {ae_rate}")
        else:
            LOGGER.error("AED rate not updated")



        self.stdout.write("Current Currency Exchange Saved Successfully.")



