from django.contrib import admin
from django.urls import path, include
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wagtail-admin/', include(wagtailadmin_urls)),
    path('accounts/', include('allauth.urls')),
    path('', include(wagtail_urls)),
]
