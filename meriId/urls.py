"""meriId URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from rest_framework_swagger.views import get_swagger_view

from meriId.views import admin_redirect

swagger_api_docs_urls = get_swagger_view(title='Meri Id API', url='/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", admin_redirect, name="admin_redirect"),
    path('api/docs/', swagger_api_docs_urls, name="api-docs"),
]


if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

admin.site.site_header = "Meri Id Admin"
admin.site.site_title = "Meri Id Admin Portal"
admin.AdminSite.index_title = "Meri Id Admin"
