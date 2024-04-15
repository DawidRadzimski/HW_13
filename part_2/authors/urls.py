from django.urls import path
from . import views

app_name = "authors"

urlpatterns = [
    path("add/", views.add, name="add"),
    path("", views.authors, name="authors"),
    path("<int:author_id>", views.details, name="details"),
    path("scrape/", views.scrape, name="scrape"),
]
