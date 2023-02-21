import django.contrib.auth.urls
from django.contrib.auth import views as auth_views
from django.urls import re_path, include, path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    re_path(r'^api/departements/', views.view_departements),
    re_path(r'^api/publications/', views.view_publications),
    re_path(r'^api/authors/', views.view_authors),
    re_path(r'^api/ssd/', views.view_ssd),
    re_path(r'^api/adu/', views.view_adu),
    re_path(r'^api/insert-professor/', views.add_professor),
    re_path(r'^api/accounts/login', views.view_login),
]
