import hashlib

from django.shortcuts import get_object_or_404, render
from sites.models import Site

from .forms import SubscriptionForm
from .models import Subscriber


def subscribe(request):
    site = Site.objects.filter(is_active=True).first()
    if not site:
        return render(request, "subscribers/status.html", {"title": "Suscripciones no disponibles", "message": "La publicación todavía no está configurada."}, status=503)
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscriber, created = Subscriber.objects.get_or_create(site=site, email=form.cleaned_data["email"].lower(), defaults=form.cleaned_data)
            if not created and subscriber.state == "active":
                return render(request, "subscribers/status.html", {"title": "Ya estás suscrito", "message": "Este correo ya recibe Blandskron Signals."})
            for field in form.fields:
                if field != "email":
                    setattr(subscriber, field, form.cleaned_data[field])
            subscriber.state = "pending"
            token = subscriber.issue_confirmation_token()
            subscriber.send_confirmation(token)
            return render(request, "subscribers/status.html", {"title": "Revisa tu correo", "message": "Te enviamos un enlace para confirmar la suscripción. El enlace vence en 48 horas."})
    else:
        form = SubscriptionForm()
    return render(request, "subscribers/subscribe.html", {"form": form})


def confirm(request, token):
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    subscriber = get_object_or_404(Subscriber, confirmation_token_hash=token_hash)
    if subscriber.confirm(token):
        return render(request, "subscribers/status.html", {"title": "Suscripción confirmada", "message": "Ya estás dentro de Blandskron Signals."})
    return render(request, "subscribers/status.html", {"title": "Enlace vencido", "message": "Solicita una nueva suscripción para recibir otro enlace."}, status=400)


def unsubscribe(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        subscriber = Subscriber.objects.filter(email=email).first()
        if subscriber:
            subscriber.unsubscribe()
        return render(request, "subscribers/status.html", {"title": "Solicitud procesada", "message": "Si el correo estaba suscrito, dejará de recibir envíos."})
    return render(request, "subscribers/unsubscribe.html")
