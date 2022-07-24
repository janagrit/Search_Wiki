from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/random", views.randomPage, name = "random"),
    path("wiki/<str:id>", views.entryInfo, name = "entryInfo"),
    path("newPage", views.newPage, name = "newPage"),
    path("search", views.searchEntry, name = "searchEntry"),
    path("wiki/<str:id>/edit", views.editPage, name = "edit"),
]
