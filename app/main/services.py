import logging
from typing import Dict, List, Union

from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail

from .forms import ContactForm
from .models import Article, Category, SubCategory
from .tasks import celery_function_test, send_email_celery

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


def _is_category_exist(cat_slug: str) -> bool:
    categories = [c.category_slug for c in Category.objects.all()]
    if cat_slug not in categories:
        logger.warning(f"Category slug {cat_slug} does not exist.")
        return False
    return True


def _is_subcategory_exist(subcat_slug: str) -> bool:
    sub_categories = [s.subcategory_slug for s in SubCategory.objects.all()]
    if subcat_slug not in sub_categories:
        logger.warning(f"Sub-category slug {subcat_slug} does not exist.")
        return False
    return True


def _is_article_exist(art_slug: str) -> bool:
    articles = [a.article_slug for a in Article.objects.all()]
    if art_slug not in articles:
        logger.warning(f"Article slug {art_slug} does not exist.")
        return False
    return True


def _get_subcategories_by_cat_slug(
    cat_slug: str,
) -> Union[List[SubCategory], None]:
    """
    Retrieves a list of SubCategory objects for a given category name.
    Filtering all SubCategory objects by cat_slug.
    """
    _ = celery_function_test.delay()

    logger.info(f"Filtering SubCategory objects by cat_slug={cat_slug}")
    # logger.info(f"Filtering SubCategory objects by cat_slug={cat_slug} -- {heya}")

    matching_sub_categories = SubCategory.objects.filter(
        category_name__category_slug=cat_slug
    )
    if len(matching_sub_categories) == 0:
        logger.warning(
            f"Category {cat_slug} does not contain any sub-category."
        )
        return None
    return matching_sub_categories


def _get_articles_by_subcat_slug(
    subcat_slug: str,
) -> Union[List[Article], None]:
    """
    Retrieves a list of Article objects for a given sub-category name.
    Filtering all Article objects by the subcat_slug.
    """
    logger.info(f"Filtering Article objects by subcat_slug={subcat_slug}")
    subcategories = [c.subcategory_slug for c in SubCategory.objects.all()]
    if subcat_slug not in subcategories:
        logger.warning(f"Sub-category {subcat_slug} does not exist.")
        return None
    matching_articles = Article.objects.filter(
        subcategory_name__subcategory_slug=subcat_slug
    )
    if len(matching_articles) == 0:
        logger.warning(
            f"Sub-category {subcat_slug} does not contain any article."
        )
        return None
    return matching_articles


def _get_urls_for_subcategories(
    sub_category_objects: List[SubCategory],
) -> Union[Dict[SubCategory, str], None]:
    """
    Input: Category slug and List of SubCategory objects
    Output: Dictionary to store the first articles URLs for each matching sub-category
        Keys: SubCategory objects
        Values: URLs to first Article for the associated SubCategory
    """
    logger.info(f"Building sub-categories URLs")
    subcategories_urls = {}
    for sub_cat in sub_category_objects:
        matching_articles = _get_articles_by_subcat_slug(
            sub_cat.subcategory_slug
        )
        if matching_articles is None:
            subcategories_urls[sub_cat] = (
                "/"
                + sub_cat.category_name.category_slug
                + "/"
                + sub_cat.subcategory_slug
            ).lower()
            continue

        try:
            first_article = matching_articles.latest("date_published")
            first_article_slug = first_article.article_slug
        except Exception:
            logger.warning(
                f"{sub_cat.subcategory_name} does not contain any article."
            )
            logger.warning(
                "Redirecting to leaving sub-category card url to /<category>/<subcategory>"
            )
            first_article_slug = ""

        # sub_cat.category_name return Categort object
        # Applying str returns name property
        subcategories_urls[sub_cat] = (
            "/"
            + sub_cat.category_name.category_slug
            + "/"
            + sub_cat.subcategory_slug
            + "/"
            + first_article_slug
        ).lower()

    if subcategories_urls is False:
        return None
    return subcategories_urls


def _send_email(request, to_emails: List[str], from_email: str) -> None:
    """
    Asynchronous task using Celery
    Send email from the contact page, using the fromemail specified.
    ToEmail variable is defined as an environmet variable in .env
    """
    form = ContactForm(request.POST)
    if not form.is_valid():
        for msg in form.error_messages:
            messages.error(request, f"{msg}: {form.error_messages[msg]}")
        logger.warning("Email form is invalid.")
        return None

    body = (
        f"Name: {form.cleaned_data['name']}\n\n"
        f"Contact email: {form.cleaned_data['contact_email']}\n\n"
        f"Message: \n{form.cleaned_data['message']}"
    )

    try:
        send_email_celery.delay(
            form.cleaned_data["subject"], body, from_email, to_emails
        )
        logger.info(f"Email task sent to celery")
        return form
    except BadHeaderError:
        logger.warning("Sending email with celery returned BadHeaderError")
        return None


# def _send_email(request, to_emails: List[str], from_email: str) -> None:
#     """
#     Synchronous task
#     Send email from the contact page, using the fromemail specified.
#     ToEmail variable is defined as an environmet variable in .env
#     """
#     form = ContactForm(request.POST)
#     if not form.is_valid():
#         for msg in form.error_messages:
#             messages.error(request, f"{msg}: {form.error_messages[msg]}")
#         logger.warning("Email form is invalid.")
#         return None

# body = (
#     f"Name: {form.cleaned_data['name']}\n\n"
#     f"Contact email: {form.cleaned_data['contact_email']}\n\n"
#     f"Message: \n{form.cleaned_data['message']}"
# )
#     try:
#         send_mail(
#             form.cleaned_data["subject"],
#             body,
#             from_email,
#             to_emails,
#             fail_silently=False,
#         )
#         logger.info(
#             f"Email sent successfully from {form.cleaned_data['name']} to {to_emails}"
#         )
#         return form
#     except BadHeaderError:
#         logger.warning("Sending email returned BadHeaderError")
#         return None
