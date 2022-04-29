from django.conf import settings

from go3xpress.core.models import Delivery
from go3xpress.utils.logger import LOGGER


def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    tracking = request.session.get('tracking')
    email = request.session.get('email')
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
        "tracking": tracking,
        "email": email,
    }
