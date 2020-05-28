import logging
from typing import List

from celery import shared_task
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task
def send_email_celery(
    subject: str, body: str, from_email: str, to_emails: List[str]
) -> None:
    """
    Celery task which calls the built-in django method django.core.mail.send_mail
    """
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
