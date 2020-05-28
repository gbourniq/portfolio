import logging
from typing import List, Union

from django.core.mail import BadHeaderError, send_mail
from django.http import Http404

from app import static_settings

from .forms import ContactForm
from .models import Category, Item
from .tasks import send_email_celery

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


def _is_category_exist(category_slug: str) -> bool:
    """
    Returns True if category object exists for a given slug, False otherwise
    """
    return (
        True
        if category_slug in [c.category_slug for c in Category.objects.all()]
        else False
    )


def get_item_in_category(
    item_slug: str, category_slug: str
) -> Union[Item, None]:
    """
    Returns an item object for a given category, and item slug
    """
    items = get_items_by_category_slug(category_slug)
    if items and item_slug in [a.item_slug for a in items]:
        return items.get(item_slug=item_slug)
    else:
        logger.warning(
            f"Item {item_slug} does not exist in category {category_slug}."
        )
        raise Http404


def get_items_by_category_slug(
    category_slug: str, ordered_by_name: bool = False
) -> Union[List[Item], None]:
    """
    Returns Item objects by the given category_slug.
    May return None is given (parent) category is not associated to any (child) item.
    """
    if not _is_category_exist(category_slug):
        logger.warning(f"Category {category_slug} does not exist.")
        raise Http404
    if ordered_by_name:
        return Item.objects.filter(
            category_name__category_slug=category_slug
        ).order_by("item_name")
    else:
        return Item.objects.filter(category_name__category_slug=category_slug)


def send_email(
    request, to_emails: List[str], from_email: str
) -> Union[None, ContactForm]:
    """
    Send an email from the contact page.
    Task may be Asynchronous depending on whether running with celery.
    Returns None is the form is invalid.
    """
    form = ContactForm(request.POST)

    if not form.is_valid():
        logger.warning("Email form is invalid.")
        return None

    body = (
        f"Name: {form.cleaned_data['name']}\n\n"
        f"Contact email: {form.cleaned_data['contact_email']}\n\n"
        f"Message: \n{form.cleaned_data['message']}"
    )

    logger.info(f"Sending email with function: {send_email_function}")

    try:
        send_email_function(
            form.cleaned_data["subject"], body, from_email, to_emails
        )
        return form
    except BadHeaderError:
        logger.warning(
            f"Email function {send_email_function} returned BadHeaderError"
        )
        return None


def send_email_function():
    """
    Set the email function to be either django.core.mail.send_mail, if REDIS_HOST
    exists, or a celery task which calls django.core.mail.send_email otherwise.
    """
    if static_settings.REDIS_HOST:
        return send_email_celery.delay
    else:
        return send_mail
