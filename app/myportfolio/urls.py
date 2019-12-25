"""myportfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
import main.views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", main.views.homepage, name="homepage"),
    re_path(r"^email/$", main.views.viewEmailForm, name="viewEmailForm"),
    re_path(r"^success/$", main.views.viewSuccessPage, name="viewSuccessPage"),
    path("admin/", admin.site.urls),
    re_path(r"^tinymce/$", include("tinymce.urls")),
    re_path(
        r"^(?P<cat_slug>[\w\-]+)/$",
        main.views.viewSubCategories,
        name="viewSubCategories",
    ),
    re_path(
        r"^(?P<cat_slug>[\w\-]+)/(?P<subcat_slug>[\w\-]+)/$",
        main.views.viewArticles,
        name="viewArticles",
    ),
    re_path(
        r"^(?P<cat_slug>[\w\-]+)/(?P<subcat_slug>[\w\-]+)/(?P<article_slug>[\w\-]+)/$",
        main.views.viewArticle,
        name="viewArticle",
    ),
]

urlpatterns = (
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + urlpatterns
)
