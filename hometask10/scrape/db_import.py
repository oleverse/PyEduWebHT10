import logging

import django.db
import django.db.models

from . import models as scrape_models
from locale import setlocale, LC_ALL
from datetime import datetime

from django.apps import apps
from django.template.defaultfilters import slugify

DB_AUTHOR_MODEL = apps.get_model('quoteapp', 'Author')
DB_QUOTE_MODEL = apps.get_model('quoteapp', 'Quote')
DB_TAG_MODEL = apps.get_model('quoteapp', 'Tag')
logger = logging.getLogger(__name__)


setlocale(LC_ALL, 'en_US.UTF-8')


def import_authors(authors_list: list[scrape_models.Author]):
    successfully_saved = 0
    for author_dict in authors_list:
        new_author = DB_AUTHOR_MODEL(
            fullname=author_dict["fullname"],
            born_date=datetime.strptime(author_dict["born_date"], "%B %d, %Y").date().isoformat(),
            born_location=author_dict["born_location"],
            description=author_dict["description"],
            slug=slugify(author_dict["fullname"]).title()
        )

        try:
            new_author.save()
            successfully_saved += 1
        except django.db.Error as db_error:
            logger.error(db_error)

    return successfully_saved
    # print(f"Authors count saved to DB: {successfully_saved}")


def import_quotes(quotes_list: list[scrape_models.Quote]):
    successfully_saved = 0
    successfully_saved_tags = 0

    for quote_dict in quotes_list:
        try:
            db_author = DB_AUTHOR_MODEL.objects.get(fullname=quote_dict["author"])
        except django.db.models.DoesNotExist:
            logger.error("Author doesn't exist")
        except django.db.models.MultipleObjectsReturned:
            logger.error("There are many authors with such name.")
        else:
            for tag in quote_dict["tags"]:
                db_tag = DB_TAG_MODEL(name=tag, slug=slugify(tag))
                try:
                    db_tag.save()
                    successfully_saved_tags += 1
                except django.db.Error as db_error:
                    logger.error(db_error)

            db_tags = DB_TAG_MODEL.objects.filter(name__in=quote_dict["tags"])

            new_quote = DB_QUOTE_MODEL(
                text=quote_dict["quote"],
                author=db_author,
            )

            try:
                new_quote.save()
            except django.db.Error as db_error:
                logger.error(db_error)
            else:
                new_quote.tags.set(db_tags)
                successfully_saved += 1

    return successfully_saved, successfully_saved_tags


def import_data(authors_list: list[scrape_models.Author], quotes_list: list[scrape_models.Quote]):
    authors_saved = import_authors(authors_list)
    quotes_saved, tags_saved = import_quotes(quotes_list)

    return authors_saved, quotes_saved, tags_saved
