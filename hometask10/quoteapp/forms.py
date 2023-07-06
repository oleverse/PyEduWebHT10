from django.forms import ModelForm, CharField, TextInput, Textarea
from .models import Tag, Quote, Author


class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, max_length=250, required=True, widget=TextInput(attrs={"class": "form-control"}))
    born_location = CharField(min_length=3, max_length=250, required=True,
                              widget=TextInput(attrs={"class": "form-control"}))
    description = CharField(min_length=10, required=True, widget=Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Author
        fields = ['fullname', 'born_location', 'description']
        exclude = ['slug', 'born_date']


class QuoteForm(ModelForm):
    text = CharField(min_length=10, required=True, widget=Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Quote
        fields = ['text']
        exclude = ['tags']
