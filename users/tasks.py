from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


@shared_task
def manual_task(username):
    return f'Hello {username}'


@shared_task
def cleanup_task():
    now = timezone.now()
    send_mail(
        'Cleanup report',
        f'Cleanup executed at {now}',
        settings.DEFAULT_FROM_EMAIL,
        ['admin@example.com'],
    )
    return 'cleanup done'


@shared_task
def smtp_task(email):
    send_mail(
        'Test email',
        'This email was sent by Celery',
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
    return 'email sent'