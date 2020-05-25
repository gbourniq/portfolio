import logging

from celery import shared_task
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task
def send_email_celery(subject, body, from_email, to_emails):
    send_mail(
        subject, body, from_email, to_emails, fail_silently=False,
    )
    logger.info(
        f"""Email sent successfully via a Celery task\n
                subject: {subject}\n
                body: {body}\n
                from_email: {from_email}\n
                to_emails: {str(to_emails)}"""
    )
