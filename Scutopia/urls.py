import django.contrib.auth.urls
from django.contrib.auth import views as auth_views
from django.urls import re_path, include, path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    re_path(r'^departements/', views.view_departements),
    re_path(r'^pubblications/', views.view_pubblications),
    re_path(r'^authors/', views.view_authors),
    re_path(r'^ssd/', views.view_authors),
    re_path(r'^adu/', views.view_adu),
    re_path(r'^accounts/', include("django.contrib.auth.urls")),
]