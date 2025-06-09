from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from service_app.models import Profiles
from django.db.models.signals import post_save

@receiver(post_save, sender=Profiles)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        subject = "Willkommen bei Videoflix"
        from_email = "noreply@videoflix.de"
        context = {
            "username": instance.user.username,
            "verify_link": f"http://127.0.0.1:8000/{reverse('verify_email')}?token={instance.email_token}"
        }
        html_content = render_to_string("emails/verification_email.html", context)
        email = EmailMultiAlternatives(subject, "", from_email, [instance.user.email])
        email.attach_alternative(html_content, "text/html")
        email.send()