import logging

from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_page

from .forms import ContactForm
from .models import Category
from .services import (
    _is_category_exist,
    get_item_in_category,
    get_items_by_category_slug,
    send_email,
)

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


@cache_page(settings.CACHE_TTL)
def viewHome(request):
    """View home page"""
    return render(request, "main/home.html")


@cache_page(settings.CACHE_TTL)
def viewCategories(request):
    """View categories cards in /homepage url"""
    categories = Category.objects.all()
    if not categories:
        raise Http404
    return render(
        request,
        "main/categories.html",
        {"categories": categories.order_by("category_name")},
    )


@cache_page(settings.CACHE_TTL)
def viewItems(request, category_slug: str) -> None:
    """
    Requests at /<category>/ are redirected to /<category>/<first_item>
    """
    matching_items = get_items_by_category_slug(category_slug)
    if not matching_items:
        logger.warning(f"Category {category_slug} does not contain any item.")
        raise Http404

    first_item_object = matching_items.order_by("item_name").first()
    first_item_slug = first_item_object.item_slug

    return redirect(
        viewItem, category_slug=category_slug, item_slug=first_item_slug,
    )


@cache_page(settings.CACHE_TTL)
def viewItem(request, category_slug: str, item_slug: str) -> None:
    """
    View for /<category>/<first_item>
    """
    this_item = get_item_in_category(item_slug, category_slug)
    ordered_items_in_category = get_items_by_category_slug(
        category_slug, ordered_by_name=True
    )
    this_item_idx = list(ordered_items_in_category).index(this_item)
    render_context = {
        "item": this_item,
        "sidebar": ordered_items_in_category,
        "this_item_idx": this_item_idx,
        "category_slug": category_slug,
        "category_name": this_item.category_name,
    }
    return render(request, "main/items.html", context=render_context,)


def viewContactUs(request):
    """
    View for /email where a user can send an email
    """
    if request.method == "GET":
        form = ContactForm()
        return render(request, "main/contact_us.html", {"form": form})

    if request.method == "POST":
        to_emails = [settings.EMAIL_HOST_USER]
        from_email = settings.EMAIL_HOST_USER
        form = send_email(request, to_emails, from_email)
        if not form:
            # if form invalid, stay on the same page
            return redirect(request.META["HTTP_REFERER"])
        messages.success(request, "Email sent successfully.")
        return render(
            request,
            "main/go_back_home.html",
            {"message": "Success! Thank you for your message."},
        )


def handler404(request, exception):
    return render(
        request,
        "main/go_back_home.html",
        {"message": "Oops, there's nothing here... (404)"},
    )


def handler500(request):
    return render(
        request,
        "main/go_back_home.html",
        {"message": "Internal Server Error (500)"},
    )
