from django.forms import Form, CharField, TextInput


class ScrapeForm(Form):
    site_url = CharField(min_length=10, widget=TextInput())
