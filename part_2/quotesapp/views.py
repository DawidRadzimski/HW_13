from django.shortcuts import get_object_or_404, redirect, render
from quotesapp.forms import QuoteForm
from quotesapp.models import Quote, Tag, Author
from django.core.paginator import Paginator
from scrap.scrap_quote_data import scrap_quotes


def main(request):
    return render(request, "quotesapp/index.html")


def quotes(request):
    quotes = Quote.objects.all()
    extracted_tags = [quote.tags.all() for quote in quotes]
    paginator = Paginator(list(zip(quotes, extracted_tags)), 5)
    page = request.GET.get("page")
    quotes_and_tags = paginator.get_page(page)
    return render(request, "quotesapp/display.html", {"quotes": quotes_and_tags})


def add(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotesapp:main")
        else:
            return render(request, "quotesapp/quote.html", {"form": form})

    return render(request, "quotesapp/quote.html", {"form": QuoteForm()})


def scrape(request):
    quotes = scrap_quotes()
    for quote in quotes:
        author = get_object_or_404(Author, fullname=quote.author)
        try:
            new_quote = Quote.objects.get(quote=quote.quote)
        except Quote.DoesNotExist:
            new_quote = Quote.objects.create(quote=quote.quote, author=author)
            for tagname in quote.tags:
                try:
                    tag = Tag.objects.get(name=tagname)
                except Tag.DoesNotExist:
                    tag = Tag.objects.create(name=tagname)
                new_quote.tags.add(tag)

    return redirect(to="quotesapp:quotes")
