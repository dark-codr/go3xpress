import datetime

from decimal import Decimal
import os
from django.utils import translation

from django.db.models import Sum, Q

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render

from django.conf import settings
from django.contrib import messages
from django.template.loader import get_template, render_to_string
from django.utils.safestring import mark_safe

from django.views.generic import DetailView, RedirectView, UpdateView, CreateView, ListView

from go3xpress.utils.logger import LOGGER

from .models import Delivery, DeliveryHistory, Privacy

devnull = open(os.devnull, "w")


def compress_whitespace(s):
    return " ".join(s.split())

def privacy(request):
    page = Privacy.objects.filter(is_active=True).first()
    return render(request, "pages/privacy.html", context={'page':page})

def item_detail(request, tracking):
    item = get_object_or_404(Delivery, tracking=tracking)
    track_history = DeliveryHistory.objects.filter(delivery=item)
    context = {
        'object': item,
        'track_history': track_history
    }
    return render(request, 'pages/detail.html', context)

def home(request):
    email = request.POST.get('email')
    tracking = request.POST.get('tracking')
    d_object = Delivery.objects.get(tracking=tracking) if Delivery.objects.filter(Q(tracking__iexact=tracking)).distinct() else None
    track_history = DeliveryHistory.objects.filter(delivery=d_object)
    if request.session.get('email'):
        del request.session['email']
        del request.session['tracking']
    context = {
        "tracking":tracking,
        "track_history":track_history,
        "email":email,
        "object":d_object,
    }
    if request.htmx:
        return render(request, "pages/search.html", context)
    else:
        return render(request, "pages/home.html", context)

def delivery_list(request):
    email = request.POST.get('email')
    tracking = request.POST.get('tracking')
    if request.htmx:
        d_object = Delivery.objects.get(tracking=tracking) if Delivery.objects.filter(Q(tracking__iexact=tracking)).distinct() else None
        track_history = DeliveryHistory.objects.filter(delivery=d_object)
        context = {
            "tracking":d_object.tracking,
            "track_history":track_history,
            "object":d_object,
        }
        LOGGER.info(f"Delivery Item Info: {email} {tracking} {d_object} {track_history}")
        return render(request, "pages/search.html", context)
    else:
        email = request.session.get('email')
        tracking = request.session.get('tracking')
        d_object = Delivery.objects.get(tracking=tracking) if Delivery.objects.filter(Q(tracking__iexact=tracking)).distinct() else None
        track_history = DeliveryHistory.objects.filter(delivery=d_object)
        LOGGER.info(f"Delivery Item Info: {email} {tracking} {d_object} {track_history}")
        context = {
            "tracking":d_object.tracking,
            "track_history":track_history,
            "object":d_object,
        }
        return render(request, "pages/about.html", context)





























def verify_email(request):
    email = request.GET.get('email')

    if Delivery.objects.filter(sender_email=email, delivered=False).exists() or Delivery.objects.filter(receiver_email=email, delivered=False).exists():
        request.session['email'] = email
        return HttpResponse("""<small class="block text-sm font-bold text-white" id="email">This email has a pending delivery</small>""")
    else:
        return HttpResponse("""<small class="block text-sm font-bold text-variant-2" id="email">This email has no pending delivery</small>""")

def verify_tracking(request):
    tracking = request.GET.get('tracking')

    if Delivery.objects.filter(tracking=str(tracking)).exists():
        request.session['tracking'] = tracking
        return HttpResponse("""<small class="block text-sm font-bold text-white" id="result">This item is available</small>""")
    else:
        return HttpResponse("""<small class="block text-sm font-bold text-variant-2" id="result">This tracking item does not exists</small>""")


def switch_language(request, **kwargs):
    language = kwargs.get('language')
    redirect_url_name = request.GET.get('url') # e.g. '/about/'

    # make sure language is available
    valid = False
    for l in settings.LANGUAGES:
        if l[0] == language:
            valid = True
    if not valid:
        raise Http404(_('The selected language is unavailable!'))

    # Make language the setting for the session
    translation.activate(language)
    # response = redirect(reverse(redirect_url_name)) # Changing this to use reverse works

    # response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    # return response
    return redirect(reverse(language, kwargs={'url':redirect_url_name})) # Changing this to use reverse works

