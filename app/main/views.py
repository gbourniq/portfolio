import logging

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from main.models import Article, Category, SubCategory
from main.utils.views_utils import (
    _get_articles_by_subcat_slug,
    _get_subcategories_by_cat_slug,
    _get_urls_for_subcategories,
    _is_article_exist,
    _send_email,
)

from .forms import ContactForm

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


# Create your views here.
def homepage(request):
    """View for /homepage url"""
    categories = Category.objects.all
    logger.info("Homepage")
    return render(request, "main/categories.html", {"categories": categories})


def viewSubCategories(request, cat_slug: str) -> None:
    """
    View for a /<category> url
    Redirect to page where User can click on sub-category cards
    """
    logger.info(f"GET request to /{cat_slug}")

    matching_sub_categories = _get_subcategories_by_cat_slug(cat_slug)
    if len(matching_sub_categories) == 0 or matching_sub_categories is None:
        logger.info(f"No sub-category for /{cat_slug}.")
        logger.info(f"Redirecting to /.")
        return redirect(homepage)
    subcategories_urls = _get_urls_for_subcategories(matching_sub_categories)
    if subcategories_urls is None:
        HttpResponse(f"No sub-category could be retrieved.")

    return render(
        request,
        "main/subcategories.html",
        {
            "subcategories_urls": subcategories_urls,
            "category_name": Category.objects.filter(
                category_slug=cat_slug
            ).first(),
        },
    )


def viewArticles(request, cat_slug: str, subcat_slug: str) -> None:
    """
    If user manually goes to /<category>/<sub-category>/ url
    It will be redirected to /<category>/<sub-category>/<first_article>
    """
    matching_articles = _get_articles_by_subcat_slug(subcat_slug)
    if len(matching_articles) == 0:
        logger.info(f"No articles for /{cat_slug}/{subcat_slug}/.")
        logger.info(f"Redirecting to /{cat_slug}.")
        return redirect(viewSubCategories, cat_slug=cat_slug)

    first_article = matching_articles.latest("date_published")
    first_article_slug = first_article.article_slug

    return redirect(
        viewArticle,
        cat_slug=cat_slug,
        subcat_slug=subcat_slug,
        article_slug=first_article_slug,
    )


def viewArticle(request, cat_slug, subcat_slug, article_slug) -> None:
    """
    View for a /<category>/<sub-category>/<article-name> url
    After user clicked on a sub-category card or article list item
    """

    logger.info(f"GET request to /{cat_slug}/{subcat_slug}/{article_slug}")

    if not _is_article_exist:
        return HttpResponse(
            f"{cat_slug}/{subcat_slug}/{article_slug} does not seem to be a valid path."
        )

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


def viewEmailForm(request):
    """
    View for /email url
    Allows a user to send an email
    """
    if request.method == "GET":
        form = ContactForm()
        return render(request, "main/email.html", {"form": form})

    if request.method == "POST":
        form = _send_email(request)
        if not form:
            return HttpResponse("Invalid header found.")
        messages.success(request, "Email sent successfully.")
        return redirect("success")


def viewSuccessPage(request):
    """
    View for /success url
    Page to confirm the email has been sent successfully
    """
    return render(request, "main/emailsuccess.html")
