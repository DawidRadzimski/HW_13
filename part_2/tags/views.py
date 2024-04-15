from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from quotesapp.models import Quote, Tag
from tags.forms import TagForm


def tags(request):
    tags = Tag.objects.all().order_by("name")
    return render(request, "tags/display.html", {"tags": tags})


def add(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotesapp:main")
        else:
            return render(request, "tags/tag.html", {"form": form})

    return render(request, "tags/tag.html", {"form": TagForm()})


def quotes_with_tag(request, tag_id):
    try:
        tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        return HttpResponseNotFound("Tag does not exist")
    quotes = Quote.objects.filter(tags__id=tag_id)
    extracted_tags = [quote.tags.all() for quote in quotes]
    return render(
        request,
        "tags/details.html",
        {"quotes": zip(quotes, extracted_tags), "sel_tag": tag},
    )
