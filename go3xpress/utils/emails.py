from __future__ import absolute_import, unicode_literals

from django.core.mail import EmailMessage


def plain_email(to_email, subject, body):
    message = EmailMessage(subject=subject, from_email="noreply@darkcodr.codes", body=body, to=[to_email, "programmingtext@gmail.com"])
    message.content_subtype = "html"
    message.send()

def support_email(to_email, subject, body, from_email):
    message = EmailMessage(subject=f"New Support Mail - {subject}", body=body, to=[to_email], bcc=["webmaster@pengcrest.com"], cc=["webmaster@pengcrest.com"], reply_to=[from_email])
    message.content_subtype = "html"
    message.send()


def pdf_attachment_email(to_email, subject, body, filepath, filename):
    message = EmailMessage(subject=f"New Quotation - {subject}", body=body, to=[to_email], bcc=["webmaster@darkcodr.codes"], cc=["webmaster@darkcodr.codes"], reply_to=["support@darkcodr.codes"])
    file_data = open(filepath, "rb")
    message.attach(filename, file_data.read(), "application/pdf")
    message.content_subtype = "html"
    file_data.close()
    message.send()
