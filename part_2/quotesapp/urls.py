from django.urls import path
from . import views

app_name = "quotesapp"

urlpatterns = [
    path("", views.main, name="main"),
    path("quotes/", views.quotes, name="quotes"),
    path("quotes/add/", views.add, name="add"),
    path("quotes/scrape/", views.scrape, name="scrape"),
]
