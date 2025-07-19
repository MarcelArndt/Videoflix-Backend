from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from service_app.models import Profiles

def send_validation_email(profil_id):
    profil = Profiles.objects.get(id = profil_id)
    subject = "Willkommen bei Videoflix"
    from_email = "noreply@videoflix.de"
    context = {
        "username": profil.user.username,
        "verify_link": f"http://127.0.0.1:8000/api/verify-email/?token={profil.email_token}"
    }
    html_content = render_to_string("emails/verification_email.html", context)
    email = EmailMultiAlternatives(subject, "", from_email, [profil.user.email])
    email.attach_alternative(html_content, "text/html")
    email.send()