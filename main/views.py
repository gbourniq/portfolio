from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, SubCategory, Category
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from .forms import ContactForm
import datetime



# Create your views here.
def homepage(request):
    categories = Category.objects.all
    return render(request, "main/categories.html", {"categories": categories})


def category(request, cat_slug):
    print(f"Category request received\nCategory slug: {cat_slug}")

    categories = [c.category_slug for c in Category.objects.all()]
    if cat_slug in categories:
        matching_sub_categories = SubCategory.objects.filter(
            category_name__category_slug=cat_slug
        )

        # Dictionary to store the first articles URLs for each matching sub category
        subcategories_urls = {}
        for sub_cat in matching_sub_categories:
            try:
                all_articles = Article.objects.filter(
                    subcategory_name__subcategory_name=sub_cat
                )
                first_article = all_articles.earliest("date_published")
                first_article_slug = first_article.article_slug
                full_path = (
                    "/"
                    + cat_slug
                    + "/"
                    + sub_cat.subcategory_slug
                    + "/"
                    + first_article_slug
                )
                subcategories_urls[sub_cat] = full_path
            except Exception as e:
                print(f"Sub-category {sub_cat} may not contain any article.")

        return render(
            request,
            "main/subcategories.html",
            {
                "first_articles_urls": subcategories_urls,
                "cat_name": Category.objects.filter(category_slug=cat_slug).first(),
            },
        )

    return HttpResponse(f"{cat_slug} does not correspond to anything!!")


def subcategory(request, cat_slug, subcat_slug):
    print("Sub category request received\n")
    print(f"category slug: {cat_slug}")
    print(f"sub category slug: {subcat_slug}")

    subcats_slugs = [s.subcategory_slug for s in SubCategory.objects.all()]
    if subcat_slug in subcats_slugs:
        all_articles = Article.objects.filter(
            subcategory_name__subcategory_slug=subcat_slug
        )
        first_article = all_articles.earliest("date_published")
        first_article_slug = first_article.article_slug

        article(request, cat_slug, subcat_slug, first_article_slug)

    return HttpResponse(f"{cat_slug}/{subcat_slug} does not correspond to anything!!")


def article(request, cat_slug, subcat_slug, article_slug):
    print("Article request received\n")
    print(f"category slug: {cat_slug}")
    print(f"sub category slug: {subcat_slug}")
    print(f"article slug: {article_slug}")

    articles_slugs = [a.article_slug for a in Article.objects.all()]
    if article_slug in articles_slugs:
        this_article = Article.objects.get(article_slug=article_slug)
        all_articles = Article.objects.filter(
            subcategory_name=this_article.subcategory_name
        ).order_by("date_published")
        article_subcategory = SubCategory.objects.filter(
            subcategory_name=all_articles.first().subcategory_name
        )
        article_category = Category.objects.filter(
            category_name=article_subcategory.first().category_name
        )

        if (
            article_slug == this_article.article_slug
            and subcat_slug == article_subcategory.first().subcategory_slug
            and cat_slug == article_category.first().category_slug
        ):

            this_tutorial_idx = list(all_articles).index(this_article)
            return render(
                request,
                "main/articles.html",
                context={
                    "article": this_article,
                    "sidebar": all_articles,
                    "this_tutorial_idx": this_tutorial_idx,
                    "cat_slug": cat_slug,
                    "subcat_slug": subcat_slug,
                    "cat_name": Category.objects.filter(category_slug=cat_slug)
                    .first()
                    .category_name,
                    "subcat_name": SubCategory.objects.filter(
                        subcategory_slug=subcat_slug
                    )
                    .first()
                    .subcategory_name,
                },
            )
    return HttpResponse(
        f"{cat_slug}/{subcat_slug}/{article_slug} does not correspond to anything!!"
    )


def emailView(request):
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            from_email = form.cleaned_data["from_email"]
            message = form.cleaned_data["message"]
            try:
                send_mail(
                    subject, message, from_email, ["guillaumebournique@gmail.com"]
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            messages.success(request, "Email sent successfully.")
            return redirect("success")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    return render(request, "main/email.html", {"form": form})


def successView(request):
    return render(request, "main/emailsuccess.html")
