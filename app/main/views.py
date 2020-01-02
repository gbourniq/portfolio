import logging

from django.conf import settings
from django.contrib import messages
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render, render_to_response
from django.views.decorators.cache import cache_page
from django.template import RequestContext

from .forms import ContactForm
from .models import Article, Category, SubCategory
from .services import (
    _get_articles_by_subcat_slug,
    _get_subcategories_by_cat_slug,
    _get_urls_for_subcategories,
    _send_email,
    _is_category_exist,
    _is_subcategory_exist,
    _is_article_exist,
)

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


@cache_page(CACHE_TTL)
def homepage(request):
    """View for /homepage url"""
    categories = Category.objects.all
    logger.info("Homepage")
    return render(request, "main/categories.html", {"categories": categories})


@cache_page(CACHE_TTL)
def viewSubCategories(request, cat_slug: str) -> None:
    """
    View for a /<category> url
    Redirect to page where User can click on sub-category cards
    """
    logger.info(f"GET request to /{cat_slug}")
    if not _is_category_exist(cat_slug):
        raise Http404
    matching_sub_categories = _get_subcategories_by_cat_slug(cat_slug)
    # import pdb; h.set_trace()
    if matching_sub_categories is None:
        logger.info(f"No sub-category for /{cat_slug}.")
        logger.info(f"Redirecting to gobackpage.html")
        return redirect(goBackPage, code=1)
    return render(
        request,
        "main/subcategories.html",
        {
            "subcategories_urls": _get_urls_for_subcategories(
                matching_sub_categories
            ),
            "category_name": Category.objects.filter(
                category_slug=cat_slug
            ).first(),
        },
    )


@cache_page(CACHE_TTL)
def viewArticles(request, cat_slug: str, subcat_slug: str) -> None:
    """
    If user manually goes to /<category>/<sub-category>/ url
    It will be redirected to /<category>/<sub-category>/<first_article>
    """
    if not _is_category_exist(cat_slug) and not _is_subcategory_exist(
        subcat_slug
    ):
        raise Http404

    matching_articles = _get_articles_by_subcat_slug(subcat_slug)
    if matching_articles is None:
        logger.info(f"No articles for /{cat_slug}/{subcat_slug}/.")
        logger.info(f"Redirecting to gobackpage.html")
        return redirect(goBackPage, code=2)

    first_article = matching_articles.latest("date_published")
    first_article_slug = first_article.article_slug

    return redirect(
        viewArticle,
        cat_slug=cat_slug,
        subcat_slug=subcat_slug,
        article_slug=first_article_slug,
    )


@cache_page(CACHE_TTL)
def viewArticle(request, cat_slug, subcat_slug, article_slug) -> None:
    """
    View for a /<category>/<sub-category>/<article-name> url
    When user clicked on a sub-category card or article list item
    """

    logger.info(f"GET request to /{cat_slug}/{subcat_slug}/{article_slug}")

    if (
        not _is_category_exist(cat_slug)
        and not _is_subcategory_exist(subcat_slug)
        and not _is_article_exist(article_slug)
    ):
        raise Http404

    this_article = Article.objects.get(article_slug=article_slug)
    all_articles = (
        Article.objects.filter(subcategory_name=this_article.subcategory_name)
        .order_by("date_published")
        .reverse()
    )
    this_tutorial_idx = list(all_articles).index(this_article)

    this_cat_name = Category.objects.get(category_slug=cat_slug).category_name
    this_subcat_name = SubCategory.objects.get(
        subcategory_slug=subcat_slug
    ).subcategory_name

    render_context = {
        "article": this_article,
        "sidebar": all_articles,
        "this_tutorial_idx": this_tutorial_idx,
        "cat_slug": cat_slug,
        "subcat_slug": subcat_slug,
        "cat_name": this_cat_name,
        "subcat_name": this_subcat_name,
    }

    return render(request, "main/articles.html", context=render_context,)


def contactPage(request):
    """
    View for /email url
    Allows a user to send an email
    """
    if request.method == "GET":
        form = ContactForm()
        return render(request, "main/email.html", {"form": form})

    if request.method == "POST":
        to_emails = [settings.EMAIL_HOST_USER]
        from_email = settings.EMAIL_HOST_USER
        form = _send_email(request, to_emails, from_email)
        if not form:
            # if form invalid, stay on the same page
            return redirect(request.META["HTTP_REFERER"])
        messages.success(request, "Email sent successfully.")
        return redirect(goBackPage, code=3)


def goBackPage(request, code):
    """
    View for /success url
    Page to confirm the email has been sent successfully
    """
    msg_mapping = {
        "1": "No sub-category item(s) to display.",
        "2": "No article item(s) to display.",
        "3": "Success! Thank you for your message.",
    }
    if code not in msg_mapping:
        raise Http404

    return render(
        request, "main/gobackpage.html", {"message": msg_mapping[code]}
    )


def handler404(request, exception, template_name="main/404.html"):
    response = render_to_response("main/404.html")
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render_to_response(
        "main/500.html", {}, context_instance=RequestContext(request)
    )
    response.status_code = 500
    return response
