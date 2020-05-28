import logging
from typing import Union

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
def viewHome(request) -> render:
    """View for home page, /homepage"""
    return render(request, "main/home.html")


@cache_page(settings.CACHE_TTL)
def viewCategories(request) -> render:
    """View for categories cards - /items"""
    categories = Category.objects.all()
    if not categories:
        raise Http404
    return render(
        request,
        "main/categories.html",
        {"categories": categories.order_by("category_name")},
    )


@cache_page(settings.CACHE_TTL)
def viewItems(request, category_slug: str) -> redirect:
    """
    Requests to /<category>/ are redirected to /<category>/<first_item>/
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
def viewItem(request, category_slug: str, item_slug: str) -> render:
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


def viewContactUs(request) -> Union[render, redirect]:
    """
    View for /email, display the contact form.
    Stays on the same page if the submitted form is invalid.
    """
    if request.method == "GET":
        return render(request, "main/contact_us.html", {"form": ContactForm()})

    if request.method == "POST":
        if not send_email(
            request, [settings.EMAIL_HOST_USER], settings.EMAIL_HOST_USER
        ):
            return redirect(request.META["HTTP_REFERER"])
        else:
            messages.success(request, "Email sent successfully.")
            return render(
                request,
                "main/go_back_home.html",
                {"message": "Success! Thank you for your message."},
            )


def handler404(request, exception) -> render:
    """Function to handle any 404 error with a custom page"""
    return render(
        request,
        "main/go_back_home.html",
        context={
            "message": "Oops, there's nothing here... (404)",
            "code_handled": 404,
        },
    )


def handler500(request):
    """Function to handle any 500 error with a custom page"""
    return render(
        request,
        "main/go_back_home.html",
        context={
            "message": "Internal Server Error (500)",
            "code_handled": 500,
        },
    )
