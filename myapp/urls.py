from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

from myapp import views

urlpatterns = [
    path('', views.home),
    path('\edit', views.edit),
]
