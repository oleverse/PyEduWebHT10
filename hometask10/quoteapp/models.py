import re

from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=250, null=False, unique=True)
    slug = models.CharField(max_length=250, null=False)

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    fullname = models.CharField(max_length=250, null=False)
    born_date = models.DateField(null=True, auto_now_add=False)
    born_location = models.CharField(max_length=250, null=True)
    description = models.TextField(null=True)
    added = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=250, null=False)

    class Meta:
        unique_together = ['fullname', 'born_date']

    def __str__(self):
        return f"{self.fullname}"


class Quote(models.Model):
    text = models.TextField(null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['text', 'author']

    def __str__(self):
        return f'{self.text}'
