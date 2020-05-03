import logging
from typing import List, Union

from django.core.mail import BadHeaderError, send_mail
from django.http import Http404

from static_settings import REDIS_HOST

from .forms import ContactForm
from .models import Category, Item
from .tasks import send_email_celery

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


def _is_category_exist(category_slug: str) -> bool:
    """
    Returns True if category object exists for a given slug.
    Returns False otherwose
    """
    categories = [c.category_slug for c in Category.objects.all()]
    if category_slug not in categories:
        return False
    return True


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
    May return None is given category does not contain any item.
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


def send_email(request, to_emails: List[str], from_email: str) -> None:
    """
    Send email from the contact page, using the fromemail specified.
    ToEmail variable is defined as an environment variable in .env
    Task may be Asynchronous depending on whether running with celery
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

    send_email_function = send_email_celery.delay if REDIS_HOST else send_mail
    try:
        send_email_function(
            form.cleaned_data["subject"],
            body,
            from_email,
            to_emails,
            fail_silently=False,
        )
        return form
    except BadHeaderError:
        logger.warning(
            f"Email function {send_email_function} returned BadHeaderError"
        )
        return None
