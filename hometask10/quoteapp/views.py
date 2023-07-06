import django.db
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm
from .models import Tag, Quote, Author
from django.conf import settings
from datetime import datetime
from django.template.defaultfilters import slugify


# Create your views here.
def get_pagination_values(model_obj, page_number):
    page_number = int(page_number)
    offset = (page_number - 1) * settings.QUOTES_PER_PAGE
    model_obj_subset = model_obj[offset:offset + settings.QUOTES_PER_PAGE]
    next_quotes_set = model_obj[offset + settings.QUOTES_PER_PAGE:offset + settings.QUOTES_PER_PAGE * 2]
    next_page_number = page_number + 1 if len(next_quotes_set) else 0
    prev_page_number = page_number - 1 if page_number > 1 else 0

    return model_obj_subset, prev_page_number, next_page_number


def main(request, page_number=1):
    quotes = Quote.objects.all().order_by('-added')

    quotes, prev_page_number, next_page_number = get_pagination_values(quotes, page_number)

    return render(request, 'quoteapp/index.html', {
        'quotes': quotes, 'next_page': next_page_number, 'prev_page': prev_page_number
    })


def tag(request, tag_slug, page_number=1):
    tag = get_object_or_404(Tag, slug=tag_slug)
    quotes = tag.quote_set.all().order_by('id')

    quotes, prev_page_number, next_page_number = get_pagination_values(quotes, page_number)

    return render(request, 'quoteapp/tag.html', {
        'tag': tag, 'path': request.path, 'quotes': quotes,
        'next_page': next_page_number, 'prev_page': prev_page_number
    })


def author(request, author_slug):
    author = get_object_or_404(Author, slug=author_slug)
    return render(request, 'quoteapp/author.html', {'author': author})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save(commit=False)
            new_author.born_date = datetime.fromisoformat(request.POST['born_date'])
            new_author.slug = slugify(new_author.fullname).title()
            try:
                new_author.save()
            except django.db.Error:
                author_successfully_added = 'The author exists!'
            else:
                author_successfully_added = 'The author has been successfully added!'

            return render(request, 'quoteapp/add-author.html', {
                'form': AuthorForm(),
                'author_successfully_added': author_successfully_added
            })
        else:
            return render(request, 'quoteapp/add-author.html', {'form': form})

    return render(request, 'quoteapp/add-author.html', {'form': AuthorForm()})


@login_required
def add_quote(request):
    tags = Tag.objects.order_by('name').all()
    authors = Author.objects.order_by('fullname').all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.author = Author.objects.get(pk=request.POST['author'])
            new_quote.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            quote_successfully_added = 'The quote has been successfully added!'
            return render(request, 'quoteapp/add-quote.html', {
                "tags": tags, 'authors': authors, 'form': QuoteForm(),
                'quote_successfully_added': quote_successfully_added
            })
        else:
            return render(request, 'quoteapp/add-quote.html', {"tags": tags, 'authors': authors, 'form': form})

    return render(request, 'quoteapp/add-quote.html', {"tags": tags, 'authors': authors, 'form': QuoteForm()})
