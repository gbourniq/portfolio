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
from django.urls import path, include
import main.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", main.views.homepage, name="homepage"),
    path("email/", main.views.emailView, name="email"),
    path("success/", main.views.successView, name="success"),
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("<str:cat_slug>/", main.views.category, name="category"),
    path(
        "<str:cat_slug>/<str:subcat_slug>/",
        main.views.subcategory,
        name="subcategory",
    ),
    path(
        "<str:cat_slug>/<str:subcat_slug>/<str:article_slug>/",
        main.views.article,
        name="article",
    ),
]

urlpatterns = (
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + urlpatterns
)
urlpatterns = (
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
)
