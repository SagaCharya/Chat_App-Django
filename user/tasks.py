from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_verification_email(email, verification_link):
    send_mail(
        'Verify Your Mail',
        f'Click the link to verify your Email:{verification_link}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )

@shared_task
def send_password_change_email(email, verification_link):
    send_mail(
        'Verify Your Mail',
        f'Click the link to Change your password:{verification_link}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )