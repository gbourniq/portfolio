"""portfolio URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

import main.views

urlpatterns = [
    path("", main.views.homepage, name="homepage"),
    re_path(r"^contact/$", main.views.contactPage, name="contactPage"),
    re_path(
        r"^info/(?P<code>[\w\-]+)/$", main.views.goBackPage, name="goBackPage"
    ),
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
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

# Custom views for 404 and 500
handler404 = "main.views.handler404"
handler500 = "main.views.handler500"
