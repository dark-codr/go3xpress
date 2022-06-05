

import datetime
from django.core.mail import EmailMessage
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from go3xpress.core.models import Delivery, DeliveryHistory
from go3xpress.utils.emails import plain_email
from go3xpress.utils.unique_generators import unique_tracking_generator


@receiver(pre_save, sender=Delivery)
def create_tracknumber(sender, instance, *args, **kwargs):
    if not instance.tracking:
        instance.tracking = unique_tracking_generator(instance)
        body = f"""
        Hello {instance.sender_name.title()},
        <br>
        <br>
        Your Item from {instance.from_loc.title()} to {instance.to_loc.title()} has been shipped.
        <br>
        <br>
        Here is your item tracking number.
        <br>
        <br>
        __________________________________
        <br>
        <br>
        {instance.tracking}
        <br>
        __________________________________
        <br>
        <br>
        use this tracking number to track your item, or click on the link below to immediately track your item location.
        <br>
        <br>
        <a href="http://go3xpress.com/en/delivery/{instance.tracking}">http://go3xpress.com/en/delivery/{instance.tracking}</a>
        <br>
        <br>
        Team Go3Xpress
        """
        message = get_template('mail/simple_mail.html').render(context={"subject": "Item Tracking Number", "body": mark_safe(body)})
        plain_email(to_email=instance.sender_email, subject="Item Tracking Number", body=message)

@receiver(post_save, sender=Delivery)
def post_save_signal(sender, instance, *args, **kwargs):
    if instance.delivered:
        instance.delivered_date = datetime.now()
        body = f"""
        Hello {instance.sender_name.title()},
        <br>
        <br>
        Your item with tracking number.
        <br>
        <br>
        __________________________________
        <br>
        {instance.tracking}
        <br>
        <br>
        Has been delivered
        <br>
        <br>
        Date: {instance.delivered_date}
        <br>
        __________________________________
        <br>
        <br>
        use this tracking number to track your item, or click on the link below to immediately track your item location.
        <br>
        <br>
        <a href="http://go3xpress.com/en/delivery/{instance.tracking}">http://go3xpress.com/en/delivery/{instance.tracking}</a>
        <br>
        <br>
        Team Go3Xpress
        """
        message = get_template('mail/simple_mail.html').render(context={"subject": f"Item {instance.tracking} Delivered", "body": mark_safe(body)})
        plain_email(to_email=instance.sender_email, subject=f"Item {instance.tracking} Delivered", body=message)

    if instance.last_loc:
        DeliveryHistory.objects.create(delivery=instance, last_loc=instance.last_loc)
        body = f"""
        Hello {instance.sender_name.title()},
        <br>
        <br>
        Your Item Just arrived at the location below.
        <br>
        <br>
        __________________________________
        <br>
        <br>
        {instance.tracking}
        {instance.last_loc}
        <br>
        __________________________________
        <br>
        <br>
        use this tracking number to track your item, or click on the link below to immediately track your item location.
        <br>
        <br>
        <a href="http://go3xpress.com/en/delivery/{instance.tracking}">http://go3xpress.com/en/delivery/{instance.tracking}</a>
        <br>
        <br>
        Team Go3Xpress
        """
        message = get_template('mail/simple_mail.html').render(context={"subject": f"Item {instance.tracking} Arrived at {instance.last_loc}", "body": mark_safe(body)})
        plain_email(to_email=instance.sender_email, subject=f"Item {instance.tracking} Arrived at {instance.last_loc}", body=message)
