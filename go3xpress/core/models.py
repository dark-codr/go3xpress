from __future__ import absolute_import

# development system imports
import os
import datetime
import random
import uuid
# from datetime import date, datetime, timedelta
from decimal import Decimal
from django.core.mail import EmailMessage

# Third partie imports
from dateutil import relativedelta
# django imports
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    EmailField,
    FileField,
    FloatField,
    ForeignKey,
    GenericIPAddressField,
    ImageField,
    IntegerField,
    OneToOneField,
    SlugField,
    TextChoices,
    TextField,
    URLField,
    UUIDField,
)
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from django_resized import ResizedImageField
from model_utils.models import TimeStampedModel

from go3xpress.utils.unique_generators import (
    unique_tracking_generator,
)
from tinymce import HTMLField

def get_date():
    return timezone.now()

class Privacy(TimeStampedModel):
    title = CharField(max_length=255, unique=True)
    content = TextField(blank=True, null=True)
    is_active = BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Privacy"
        verbose_name_plural = "Privacy"

class Delivery(TimeStampedModel):
    SERVICES = (
        ('Confidential Doc', 'Documents'),
        ('International Delivery', 'International Delivery'),
        ('Pet Shifting', 'Pets Shifting'),
        ('Fragile Item', 'Fragile Item'),
        ('Vehicle Deliveries', 'Vehicle Deliveries'),
    )

    sender_name = CharField(_("Sender Name"), max_length=250, null=True, blank=True)
    sender_address = CharField(_("Sender Address"), max_length=250, null=True, blank=True)
    sender_phone = CharField(_("Sender Phone"), max_length=13, null=True, blank=True)
    sender_email = EmailField(_("Sender Email"), null=True, blank=True,)

    receiver_name = CharField(_("Receiver Name"), max_length=500, null=True, blank=True)
    receiver_address = CharField(_("Receiver Address"), max_length=500, null=True, blank=True)
    receiver_phone = CharField(_("Receiver Phone"), max_length=13, null=True, blank=True)
    receiver_email = EmailField(_("Receiver Email"), null=True, blank=True,)

    tracking = CharField(_("Tracking Number"), max_length=50, null=True, blank=True)

    services = CharField(_("Shipping Services"), max_length=500, null=True, blank=True, choices=SERVICES, default="International Delivery")

    quantity = IntegerField(_("Quantity"), default=1)
    weight = FloatField(_("Weight"), default=1.00)
    from_loc = CharField(_("Pickup Address"), max_length=500, null=True, blank=True)
    to_loc = CharField(_("Dropoff Address"), max_length=500, null=True, blank=True)

    last_loc = CharField(_("Last Location"), max_length=500, null=True, blank=True)

    # admin fields
    when_to_deliver = DateTimeField(_("Delivery Date"), default=get_date)
    departure_date = DateTimeField(_("Departure date"), default=get_date)
    delivered_date = DateTimeField(_("Arrival date"), default=get_date)

    cost = DecimalField(_("Shipping Cost"), decimal_places=2, max_digits=20, default=0.00)

    delivered = BooleanField(default=False)
    delayed = BooleanField(default=False)
    held = BooleanField(default=False)

    def __str__(self):
        return f"{self.sender_name} - {self.receiver_name}"

    def delayed(self):
        if timezone.now() > self.when_to_deliver or self.held:
            self.delayed = True
            self.save()
            return True
        else:
            return False

    class Meta:
        managed = True
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"
        ordering = ["-created", "-modified"]

    def get_absolute_url(self):
        """Get url for delivery detail view.

        Returns:
            str: URL for delivery detail view.

        """
        return reverse("items:detail", kwargs={"tracking": self.tracking})

    def all_items(self):
        return self.items_set.all()


    def get_update_url(self):
        return f"{self.get_absolute_url}/update"

    def get_delete_url(self):
        return f"{self.get_absolute_url}/delete"

class Items(TimeStampedModel):
    delivery = ForeignKey(Delivery, on_delete=CASCADE)
    item_name = CharField(_("Item Name"), max_length=500, null=True, blank=True)
    content = TextField(blank=True, null=True)
    weight = FloatField(_("Weight"), default=1.00)

    def __str__(self):
        return self.item_name

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"


class DeliveryHistory(models.Model):
    delivery = ForeignKey(Delivery, on_delete=SET_NULL, null=True)
    date = DateTimeField(auto_now_add=True)
    last_loc = CharField(_("Last Location"), max_length=500, null=True, blank=True)

    def __str__(self):
        return self.delivery.item_name

class Currency(TimeStampedModel):
    NGN = "NGN"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CNY = "CNY"
    JPY = "JPY"
    AUD = "AUD"
    CAD = "CAD"
    CHF = "CHF"
    DKK = "DKK"
    SEK = "SEK"
    ZAR = "ZAR"
    AED = "AED"
    CODE = (
        (NGN, "Nigerian Naira"),
        (USD, "United States Dollar"),
        (EUR, "Euro"),
        (GBP, "British Pound"),
        (CNY, "Chinese Yuan"),
        (JPY, "Japanese Yen"),
        (AUD, "Australian Dollar"),
        (CAD, "Canadian Dollar"),
        (CHF, "Swiss Franc"),
        (DKK, "Danish Krone"),
        (SEK, "Swedish Krona"),
        (ZAR, "South African Rand"),
        (AED, "United Arab Emirates Dirham"),
    )
    code = CharField(max_length=3, choices=CODE, default=USD, blank=False, null=False, unique=True)
    symbol = CharField(max_length=10, blank=False, null=False, unique=True)
    price = DecimalField(max_digits=20, decimal_places=2, blank=False, default=0.00, null=False)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")
        ordering = ["code"]


