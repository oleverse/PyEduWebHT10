from django.shortcuts import render
from .parser import QuotesParser
from .forms import ScrapeForm
from .db_import import import_data


def main(request):
    site_url = 'https://quotes.toscrape.com'

    if request.method == 'POST':
        form = ScrapeForm(request.POST)
        report = None
        if form.is_valid():
            parser = QuotesParser(request.POST["site_url"])
            report = [item.strip() for item in parser.parse_data()]

            authors_report, authors_list = parser.authors
            report.append(authors_report)

            quotes_report, quotes_list = parser.quotes
            report.append(quotes_report)

            authors_saved, quotes_saved, tags_saved = import_data(authors_list, quotes_list)

            report.append(f'Authors added to DB: {authors_saved}')
            report.append(f'Quotes added to DB: {quotes_saved}')
            report.append(f'Tags added to DB: {tags_saved}')

        return render(request, 'scrape/scrape_quotes.html', {'form': form, 'report': report})

    return render(request, 'scrape/scrape_quotes.html', {'form': ScrapeForm(initial={'site_url': site_url})})
