"""coolsite URL Configuration

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
from typing import Pattern
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from coolsite.settings import STATIC_ROOT, STATIC_URL, STATICFILES_DIRS
from coolsite import settings
from women.views import *

# from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path("captcha/", include("captcha.urls")),
    path("", include("women.urls")),
]
if settings.DEBUG:
    import debug_toolbar

    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# В процессе отладки сайта, то есть, когда мы используем
#  отладочный веб-сервер, нужно сэмулировать работу реального
# сервера для получения ранее загруженных файлов и передачи их
# нашему приложению
